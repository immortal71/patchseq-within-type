"""Reproduce raw vs within-type R^2 for all 29 features (M1)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from core import load_m1, cv_r2, demean, feature_frame

expr, meta, ephys = load_m1()
print("cells", expr.shape[0], "genes", expr.shape[1])
rows = []
for f in ephys.columns:
    y_all = ephys[f].dropna()
    r_all = cv_r2(expr.loc[y_all.index], y_all)
    X, y, g = feature_frame(expr, meta, ephys, f)
    r_sub = cv_r2(X, y)
    Xd, yd = demean(X, y, g)
    r_wt = cv_r2(Xd, yd)
    rows.append(dict(feature=f, n_all=len(y_all), raw_all=r_all, n_sub=len(y),
                     n_types=g.nunique(), raw_sub=r_sub, within=r_wt))
    print(f"{f:40s} raw {r_all:.3f}  raw_sub {r_sub:.3f}  within {r_wt:.4f}", flush=True)
df = pd.DataFrame(rows)
os.makedirs("results", exist_ok=True)
df.to_csv("results/m1_baseline.csv", index=False)
print(df[["raw_all", "raw_sub", "within"]].mean())
