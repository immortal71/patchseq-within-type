"""Main within-type result recomputed with type means estimated inside training folds only."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from core import load_m1, cv_r2_within, feature_frame

expr, meta, ephys = load_m1()
rows = []
for f in ephys.columns:
    X, y, g = feature_frame(expr, meta, ephys, f)
    r = cv_r2_within(X, y, g)
    rows.append(dict(feature=f, within_foldwise=r))
    print(f"{f:40s} {r:.4f}", flush=True)
df = pd.DataFrame(rows)
df.to_csv("results/m1_foldwise.csv", index=False)
print("mean", df.within_foldwise.mean())
