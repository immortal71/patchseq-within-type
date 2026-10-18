"""Within-type permutation null for all 29 features, plus family-level demeaning.

For each feature: permute the within-type residual target inside each type (500x),
refit with identical CV, p = (1 + #null >= observed) / (1 + n_perm).
Family control: same demeaning but by RNA family (types >= 15 cells kept as before).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from core import load_m1, cv_r2_multi, demean, feature_frame

N_PERM = 500
rng = np.random.default_rng(2026)
expr, meta, ephys = load_m1()
rows = []
for f in ephys.columns:
    X, y, g = feature_frame(expr, meta, ephys, f)
    Xd, yd = demean(X, y, g)
    cols = [yd.values]
    codes = g.astype("category").cat.codes.values
    for _ in range(N_PERM):
        perm = yd.values.copy()
        for c in np.unique(codes):
            idx = np.where(codes == c)[0]
            perm[idx] = perm[rng.permutation(idx)]
        cols.append(perm)
    r = cv_r2_multi(Xd, np.column_stack(cols))
    obs, null = r[0], r[1:]
    p = (1 + np.sum(null >= obs)) / (1 + N_PERM)
    fam = meta.loc[X.index, "RNA family"]
    Xf, yf = demean(X, y, fam)
    r_fam = cv_r2_multi(Xf, yf.values[:, None])[0]
    rows.append(dict(feature=f, within=obs, null_mean=null.mean(), null_95=np.quantile(null, 0.95),
                     p=p, within_family=r_fam))
    print(f"{f:40s} within {obs:.4f} null95 {np.quantile(null,0.95):.4f} p {p:.3f} fam {r_fam:.4f}", flush=True)
df = pd.DataFrame(rows)
# Benjamini-Hochberg across 29 features
m = len(df)
order = np.argsort(df.p.values)
q = np.empty(m)
q[order] = np.minimum.accumulate((df.p.values[order] * m / np.arange(1, m + 1))[::-1])[::-1]
df["q_bh"] = np.minimum(q, 1)
df.to_csv("results/m1_permutation.csv", index=False)
print("significant p<0.05:", (df.p < 0.05).sum(), " q<0.05:", (df.q_bh < 0.05).sum())
print("mean within-family R2:", df.within_family.mean())
