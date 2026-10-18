"""Calibrate observed within-type CV R^2 against known planted effect sizes.

The clean power check showed cross-validated R^2 strongly underestimates a weak planted
within-type effect at this sample size. Here, for each feature, dense linear signals of known
true R^2 are planted into a within-type-permuted copy of the residual target (real signal
removed), 30 repeats per level. The mean recovered R^2 per level gives a calibration curve;
the observed within-type R^2 is mapped back to an implied true R^2, with an interval from the
10th-90th percentile of recovered values. Also reports the smallest planted R^2 detected in
>= 80% of repeats against the feature's 95th-percentile permutation null.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from core import load_m1, cv_r2_multi, demean, feature_frame

FEATURES = ["Max number of APs", "Latency @ +20pA current (ms)", "Membrane time constant (ms)",
            "AP width (ms)", "Rebound (mV)", "AP amplitude (mV)", "Input resistance (MOhm)",
            "Upstroke-to-downstroke ratio", "Sag ratio", "Resting membrane potential (mV)"]
LEVELS = [0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40]
REPS = 30
N_NULL = 200
rng = np.random.default_rng(21)
expr, meta, ephys = load_m1()
perm_tab = pd.read_csv("results/m1_permutation.csv").set_index("feature")


def perm_within(v, codes):
    out = v.copy()
    for c in np.unique(codes):
        idx = np.where(codes == c)[0]
        out[idx] = out[rng.permutation(idx)]
    return out


rows, curves = [], []
for f in FEATURES:
    X, y, g = feature_frame(expr, meta, ephys, f)
    Xd, yd = demean(X, y, g)
    Z = ((Xd - Xd.mean()) / Xd.std().replace(0, 1)).values
    codes = g.astype("category").cat.codes.values
    null = cv_r2_multi(Xd, np.column_stack([perm_within(yd.values, codes) for _ in range(N_NULL)]))
    thr = np.quantile(null, 0.95)
    cols, labs = [], []
    for lev in LEVELS:
        for _ in range(REPS):
            base = perm_within(yd.values, codes)
            s = Z @ rng.normal(size=Z.shape[1])
            s = (s - s.mean()) / s.std() * np.sqrt(lev / (1 - lev) * base.var())
            cols.append(base + s)
            labs.append(lev)
    rec = cv_r2_multi(Xd, np.column_stack(cols))
    d = pd.DataFrame({"true": labs, "rec": rec})
    cur = d.groupby("true").rec.agg(mean="mean", lo=lambda v: np.quantile(v, .1),
                                    hi=lambda v: np.quantile(v, .9),
                                    power=lambda v: np.mean(v > thr)).reset_index()
    cur["feature"] = f
    curves.append(cur)
    obs = perm_tab.loc[f, "within"]
    tv = np.r_[0.0, cur["true"].values]
    # implied true R^2: interpolate observed on the mean / hi / lo recovery curves
    mean_c = np.r_[np.quantile(null, .5), cur["mean"].values]
    hi_c = np.r_[np.quantile(null, .9), cur["hi"].values]
    lo_c = np.r_[np.quantile(null, .1), cur["lo"].values]
    imp = np.interp(obs, mean_c, tv)
    imp_lo = np.interp(obs, hi_c, tv)   # a high recovery curve implies a smaller true value
    imp_hi = np.interp(obs, lo_c, tv)
    det80 = cur.loc[cur.power >= 0.8, "true"].min() if (cur.power >= 0.8).any() else np.nan
    raw = pd.read_csv("results/m1_baseline.csv").set_index("feature").loc[f, "raw_sub"]
    rows.append(dict(feature=f, raw_same_cells=raw, observed_within=obs, implied_true=imp,
                     implied_lo=imp_lo, implied_hi=imp_hi, min_r2_80pct_power=det80,
                     null95=thr))
    print(f"{f:32s} raw {raw:.3f} obs {obs:.4f} implied {imp:.3f} [{imp_lo:.3f}, {imp_hi:.3f}] "
          f"80%-power at {det80}", flush=True)
    print(cur.round(4).to_string(index=False), flush=True)
pd.DataFrame(rows).to_csv("results/m1_calibration.csv", index=False)
pd.concat(curves).to_csv("results/m1_calibration_curves.csv", index=False)
