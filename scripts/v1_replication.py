"""V1 replication of the within-type control (Gouwens et al. 2020 mouse VISp Patch-seq).

Run on Kaggle (or any machine that can download the Allen files). Needs three inputs:
  --features  V1_features.pickle  (github.com/berenslab/hh_sbi, code/pickles/)
  --meta      20200625_patchseq_metadata_mouse.csv   (Allen Brain Map, Mouse VISp Patch-seq)
  --counts    20200513_Mouse_PatchSeq_Release_count.csv (same release; unzip first)
These are the exact files Bernaerts et al. 2025 load in cross-validation_V1.ipynb.

Pipeline is the M1 one with one change forced by the data: the release has exon counts
only and no gene lengths, so expression is log1p(CPM) instead of log1p(RPKM).
Output: v1_within_type.csv with raw R^2, within-type R^2 and a 200x permutation p per feature.

Usage:
  python v1_replication.py --features V1_features.pickle --meta META.csv --counts COUNTS.csv
"""
import argparse
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold

ALPHAS = np.logspace(-2, 5, 30)
MIN_CELLS = 15
N_PERM = 200
PREFIXES = (
    "Kcn", "Scn", "Cacn", "Clcn", "Hcn", "Trp", "Gja", "Gjb", "Gjc", "Gjd",
    "Ano", "Best", "Asic", "P2rx", "Gabr", "Glr", "Gria", "Grik", "Grin", "Grid",
    "Chrn", "Htr3", "Ryr", "Itpr", "Piezo", "Lrrc8", "Ttyh", "Nalcn", "Orai",
    "Catsper", "Tpcn", "Hvcn", "Clic", "Zacn", "Pkd2", "Mcoln", "Cnga", "Cngb",
    "Panx", "Cftr", "Tmc", "Otop", "Calhm",
)


def cv_r2_multi(X, Y, folds=10, seed=0):
    X = np.asarray(X, float)
    Y = np.asarray(Y, float)
    if Y.ndim == 1:
        Y = Y[:, None]
    pred = np.empty_like(Y)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd[sd == 0] = 1.0
        Ztr = (X[tr] - mu) / sd
        Zte = np.clip((X[te] - mu) / sd, Ztr.min(0), Ztr.max(0))
        m = RidgeCV(alphas=ALPHAS, alpha_per_target=True).fit(Ztr, Y[tr])
        pred[te] = np.asarray(m.predict(Zte)).reshape(len(te), -1)
    return 1 - ((Y - pred) ** 2).sum(0) / ((Y - Y.mean(0)) ** 2).sum(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True)
    ap.add_argument("--meta", required=True)
    ap.add_argument("--counts", required=True)
    ap.add_argument("--out", default="v1_within_type.csv")
    a = ap.parse_args()

    d = pickle.load(open(a.features, "rb"))
    Xo = d["X_o"]
    feats = list(Xo.columns)[:-1]  # last column is the injected current, not a feature
    meta = pd.read_csv(a.meta).set_index("ephys_session_id")
    meta = meta.reindex(Xo.index.astype("int64"))
    types = meta["corresponding_AIT2.3.1_alias"]
    counts = pd.read_csv(a.counts, index_col=0).T  # cells x genes
    counts = counts.reindex(meta["transcriptomics_sample_id"].values)
    counts.index = Xo.index
    have = counts.notna().all(axis=1) & types.notna().values
    counts, Xo, types = counts[have.values], Xo[have.values], types[have.values]
    types.index = Xo.index

    lib = counts.sum(axis=1)
    genes = [g for g in counts.columns if str(g).startswith(PREFIXES)]
    expr = np.log1p(counts[genes].div(lib, axis=0) * 1e6)
    expr = expr.loc[:, (expr > 0).sum(0) >= 10]
    print("cells", len(expr), "channel genes", expr.shape[1], "types", types.nunique())

    rng = np.random.default_rng(2026)
    rows = []
    for f in feats:
        y = Xo[f].astype(float)
        ok = y.notna()
        g = types[ok]
        keep = g.map(g.value_counts()) >= MIN_CELLS
        idx = g.index[keep.values]
        X, yy, gg = expr.loc[idx], y.loc[idx], g.loc[idx]
        raw = cv_r2_multi(X, yy.values)[0]
        Xd = X - X.groupby(gg).transform("mean")
        yd = yy - yy.groupby(gg).transform("mean")
        codes = gg.astype("category").cat.codes.values
        cols = [yd.values]
        for _ in range(N_PERM):
            p = yd.values.copy()
            for c in np.unique(codes):
                ii = np.where(codes == c)[0]
                p[ii] = p[rng.permutation(ii)]
            cols.append(p)
        r = cv_r2_multi(Xd, np.column_stack(cols))
        obs, null = r[0], r[1:]
        pval = (1 + np.sum(null >= obs)) / (1 + N_PERM)
        rows.append(dict(feature=f, n=len(idx), n_types=gg.nunique(), raw=raw,
                         within=obs, null95=np.quantile(null, .95), p=pval))
        print(f"{f:28s} n {len(idx):5d} raw {raw:.3f} within {obs:.4f} p {pval:.3f}", flush=True)
    df = pd.DataFrame(rows)
    df.to_csv(a.out, index=False)
    print("\nmean raw", round(df.raw.mean(), 4), "mean within", round(df.within.mean(), 4),
          "features p<0.05:", int((df.p < 0.05).sum()), "of", len(df))


if __name__ == "__main__":
    main()
