"""Hcn test rerun on the final pipeline (specified in the preprint before the first run).

Do Hcn1-4 predict each feature within type better than random size-matched sets of
other channel genes (500 draws)? Plus leave-one-Hcn-out and Hcn1 alone.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from core import load_m1, cv_r2, demean, feature_frame

FEATURES = ["Sag ratio", "Sag time (s)", "Sag area (mV*s)", "Rebound (mV)",
            "Membrane time constant (ms)", "Resting membrane potential (mV)", "AP width (ms)"]
N_DRAW = 500
rng = np.random.default_rng(3)
expr, meta, ephys = load_m1()
hcn = [g for g in ["Hcn1", "Hcn2", "Hcn3", "Hcn4"] if g in expr.columns]
others = [g for g in expr.columns if g not in hcn]
print("Hcn genes present:", hcn)
rows = []
for f in FEATURES:
    X, y, g = feature_frame(expr, meta, ephys, f)
    Xd, yd = demean(X, y, g)
    obs = cv_r2(Xd[hcn], yd)
    null = np.array([cv_r2(Xd[list(rng.choice(others, len(hcn), replace=False))], yd)
                     for _ in range(N_DRAW)])
    p = (1 + np.sum(null >= obs)) / (1 + N_DRAW)
    rec = dict(feature=f, hcn_r2=obs, null_mean=null.mean(), null_95=np.quantile(null, .95), p=p)
    for h in hcn:
        rec[f"drop_{h}"] = cv_r2(Xd[[x for x in hcn if x != h]], yd)
    rec["hcn1_only"] = cv_r2(Xd[["Hcn1"]], yd)
    rows.append(rec)
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rec.items()}, flush=True)
pd.DataFrame(rows).to_csv("results/m1_hcn.csv", index=False)
