"""Within-type control on Bernaerts et al. (2025) fitted Hodgkin-Huxley parameters (M1).

Their preprocessing: GO ion channel genes (by symbol) + Pvalb, Lamp5, Vip, Sst; exon counts
only; genes with >= 10 total counts; counts scaled to median library size; log2(x + 1).
MAP parameters = highest-evaluation posterior sample per cell (13 parameters, 955 cells).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pickle
import numpy as np
import pandas as pd
from core import DATA, cv_r2_multi, demean, filter_groups

HH = "data/hh_sbi"
NAMES = ["C", "R_input", "tau", "g_Nat", "g_Na", "g_Kd", "g_M", "g_Kv31", "g_L",
         "E_leak", "tau_max", "VT", "r_SS"]
N_PERM = 200
rng = np.random.default_rng(5)

d = pickle.load(open(f"{HH}/code/save_model_parameters/favourite_training_schedule.pickle", "rb"))
theta = pd.DataFrame({c: d["samples"][c][int(np.argmax(np.ravel(d["evaluations"][c])))]
                      for c in d["samples"]}).T
theta.columns = NAMES

meta = pd.read_csv(os.path.join(DATA, "m1_patchseq_meta_data.csv"), sep="\t").set_index("Cell")
ex = pd.read_csv(os.path.join(DATA, "m1_patchseq_exon_counts.csv.gz"), index_col=0)
go = pd.read_csv(f"{HH}/data/GO_term_summary_20211104_075621.txt", sep="\t", index_col=False)
sel = set(go["Symbol"]) | {"Pvalb", "Lamp5", "Vip", "Sst"}
genes = [g for g in ex.index if g in sel]
X = ex.loc[genes].T
X = X.loc[:, X.sum(0) >= 10]
lib = X.sum(1)  # their notebook scales by the summed counts of the selected genes
X = np.log2(X.div(lib, axis=0) * np.median(lib) + 1)
cells = theta.index.intersection(X.index).intersection(meta.index)
X, theta, meta = X.loc[cells], theta.loc[cells], meta.loc[cells]
print("cells", len(cells), "genes", X.shape[1])

raw = cv_r2_multi(X, theta.values)
out = pd.DataFrame({"parameter": NAMES, "raw_all": raw})
for col, tag in [("RNA type", "type"), ("RNA family", "family")]:
    g = meta[col]
    keep = filter_groups(g)
    idx = g.index[keep.values]
    out[f"raw_{tag}_cells"] = cv_r2_multi(X.loc[idx], theta.loc[idx].values)
    Xd = X.loc[idx] - X.loc[idx].groupby(g[idx]).transform("mean")
    Td = theta.loc[idx] - theta.loc[idx].groupby(g[idx]).transform("mean")
    out[f"within_{tag}"] = cv_r2_multi(Xd, Td.values)
    out[f"n_{tag}"] = len(idx)
    out[f"groups_{tag}"] = g[idx].nunique()
    if tag == "type":
        codes = g[idx].astype("category").cat.codes.values
        pvals = []
        for j in range(Td.shape[1]):
            cols = [Td.values[:, j]]
            for _ in range(N_PERM):
                p = Td.values[:, j].copy()
                for c in np.unique(codes):
                    ii = np.where(codes == c)[0]
                    p[ii] = p[rng.permutation(ii)]
                cols.append(p)
            r = cv_r2_multi(Xd, np.column_stack(cols))
            pvals.append((1 + np.sum(r[1:] >= r[0])) / (1 + N_PERM))
        out["p_within_type"] = pvals
print(out.round(4).to_string())
print(out.drop(columns="parameter").mean().round(4))
out.to_csv("results/m1_hh.csv", index=False)
