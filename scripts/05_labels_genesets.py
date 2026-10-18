"""Two robustness checks on the within-type control.

(a) Label independence. The published types come from the same transcriptome that is
    being tested. Re-cluster cells from NON-channel genes only (top 3,000 variable genes
    after removing every channel gene, PCA 50, k-means k = 30 and 50) and demean by
    those clusters instead.
(b) Gene set. Replace the prefix-matched channel set with the HGNC ion channel gene
    group (human symbols mapped to mouse by case), shipped in the mini-atlas repo.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from core import DATA, PREFIXES, load_m1, cv_r2, demean, filter_groups

expr, meta, ephys = load_m1()
cells = expr.index

# ---- full matrix for clustering (exon + intron, CPM, log1p) ----
ex = pd.read_csv(os.path.join(DATA, "m1_patchseq_exon_counts.csv.gz"), index_col=0)
it = pd.read_csv(os.path.join(DATA, "m1_patchseq_intron_counts.csv.gz"), index_col=0)
it = it.reindex(index=ex.index, columns=ex.columns).fillna(0)
counts = (ex + it)[cells]
hgnc = pd.read_csv(os.path.join(DATA, "ion-channel-genes-group-177.csv"))
hgnc_mouse = {s.capitalize() for s in hgnc["Approved symbol"]}
is_channel = np.array([g.startswith(PREFIXES) or g in hgnc_mouse for g in counts.index])
cpm = counts.div(counts.sum(0), axis=1) * 1e6
logc = np.log1p(cpm.loc[~is_channel]).T
logc = logc.loc[:, (logc > 0).sum(0) >= 10]
top = logc.var().sort_values(ascending=False).index[:3000]
pcs = PCA(50, random_state=0).fit_transform((logc[top] - logc[top].mean()) / logc[top].std())
labels = {}
for k in (30, 50):
    labels[f"kmeans{k}"] = pd.Series(KMeans(k, n_init=10, random_state=0).fit_predict(pcs), index=cells).astype(str)
labels["published_type"] = meta["RNA type"]

# agreement between published types and new clusters
from sklearn.metrics import adjusted_rand_score
ok = meta["RNA type"].notna()
for k in (30, 50):
    print(f"ARI published types vs kmeans{k}: {adjusted_rand_score(meta['RNA type'][ok], labels[f'kmeans{k}'][ok]):.3f}")

# ---- HGNC gene set expression (same RPKM pipeline) ----
gl = pd.read_csv(os.path.join(DATA, "gene_lengths.txt")).set_index("GeneID")["gene_bp"]
hg = [g for g in counts.index if g in hgnc_mouse and g in gl.index]
lib = counts.sum(0)
rp = counts.loc[hg].div(gl.loc[hg] / 1e3, axis=0).div(lib / 1e6, axis=1)
expr_hgnc = np.log1p(rp).T
expr_hgnc = expr_hgnc.loc[:, (expr_hgnc > 0).sum(0) >= 10]
print("prefix genes", expr.shape[1], "HGNC genes", expr_hgnc.shape[1],
      "overlap", len(set(expr.columns) & set(expr_hgnc.columns)))

rows = []
for f in ephys.columns:
    y = ephys[f]
    rec = dict(feature=f)
    for name, lab in labels.items():
        ok = y.notna() & lab.notna()
        g = lab[ok]
        keep = filter_groups(g)
        idx = g.index[keep]
        Xd, yd = demean(expr.loc[idx], y.loc[idx], g.loc[idx])
        rec[f"within_{name}"] = cv_r2(Xd, yd)
        if name == "published_type":
            rec["raw_hgnc"] = cv_r2(expr_hgnc.loc[idx], y.loc[idx])
            Xh, yh = demean(expr_hgnc.loc[idx], y.loc[idx], g.loc[idx])
            rec["within_hgnc"] = cv_r2(Xh, yh)
        rec[f"n_{name}"] = len(idx)
    rows.append(rec)
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rec.items()}, flush=True)
df = pd.DataFrame(rows)
df.to_csv("results/m1_labels_genesets.csv", index=False)
print(df.drop(columns="feature").mean().round(4))
