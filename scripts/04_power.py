"""Power check: would the within-type pipeline detect a real within-type effect?

A known linear signal is planted into a within-type-permuted copy of the real residual
target (so any real within-type signal is removed and only the planted one remains), built from
the real within-type residual expression, at true R^2 of 0.005, 0.01, 0.02 and 0.05.
Two shapes: dense (random weights on all genes) and sparse (5 random genes).
Detection = recovered CV R^2 above the 95th percentile of that feature's within-type
permutation null (200 permutations), the same test applied to the real data.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from core import load_m1, cv_r2_multi, demean, feature_frame

FEATURES = ["Upstroke-to-downstroke ratio", "AP width (ms)", "Sag ratio",
            "Resting membrane potential (mV)"]
LEVELS = [0.005, 0.01, 0.02, 0.05, 0.10]
REPS = 25
N_NULL = 200
rng = np.random.default_rng(11)
expr, meta, ephys = load_m1()
rows = []
for f in FEATURES:
    X, y, g = feature_frame(expr, meta, ephys, f)
    Xd, yd = demean(X, y, g)
    Z = (Xd - Xd.mean()) / Xd.std().replace(0, 1)
    codes = g.astype("category").cat.codes.values
    null_cols = []
    for _ in range(N_NULL):
        perm = yd.values.copy()
        for c in np.unique(codes):
            idx = np.where(codes == c)[0]
            perm[idx] = perm[rng.permutation(idx)]
        null_cols.append(perm)
    null = cv_r2_multi(Xd, np.column_stack(null_cols))
    thr = np.quantile(null, 0.95)
    # Base target with any real within-type signal removed: one within-type permutation.
    base = yd.values.copy()
    for c in np.unique(codes):
        idx = np.where(codes == c)[0]
        base[idx] = base[rng.permutation(idx)]
    vy = base.var()
    cols, meta_rows = [], []
    for kind in ["dense", "sparse"]:
        for lev in LEVELS:
            for rep in range(REPS):
                w = np.zeros(Z.shape[1])
                if kind == "dense":
                    w = rng.normal(size=Z.shape[1])
                else:
                    w[rng.choice(Z.shape[1], 5, replace=False)] = rng.normal(size=5)
                s = Z.values @ w
                s = s - s.mean()
                s = s / s.std() * np.sqrt(lev / (1 - lev) * vy)
                cols.append(base + s)
                meta_rows.append((kind, lev, rep))
    r = cv_r2_multi(Xd, np.column_stack(cols))
    for (kind, lev, rep), val in zip(meta_rows, r):
        rows.append(dict(feature=f, kind=kind, true_r2=lev, rep=rep, recovered=val,
                         detected=val > thr, null95=thr))
    d = pd.DataFrame([x for x in rows if x["feature"] == f])
    print(f, "null95", round(thr, 4))
    print(d.groupby(["kind", "true_r2"]).agg(recovered=("recovered", "mean"),
                                             power=("detected", "mean")).round(3), flush=True)
df = pd.DataFrame(rows)
df.to_csv("results/m1_power_clean.csv", index=False)
print(df.groupby(["kind", "true_r2"]).agg(recovered=("recovered", "mean"),
                                          power=("detected", "mean")).round(3))
