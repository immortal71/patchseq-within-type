"""Check that the within-type collapse is not specific to ridge regression.

1. Elastic net per feature (penalty and l1 ratio chosen by inner 5-fold CV in each
   outer training fold), raw and within-type, same cells and outer folds as ridge.
2. Reduced-rank ridge regression at rank 2 and rank 5, fitting all 29 features
   jointly (the estimator family of Bernaerts et al. 2025), raw and within-type.
"""
import os, sys, warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNetCV, RidgeCV
from sklearn.model_selection import KFold
from sklearn.exceptions import ConvergenceWarning
from core import load_m1, demean, feature_frame, filter_groups, ALPHAS

warnings.filterwarnings("ignore", category=ConvergenceWarning)
RES = "results"
expr, meta, ephys = load_m1()


def standardize(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    Ztr = (Xtr - mu) / sd
    return Ztr, np.clip((Xte - mu) / sd, Ztr.min(0), Ztr.max(0))


def cv_enet(X, y, folds=10, seed=0):
    X, y = np.asarray(X, float), np.asarray(y, float)
    pred = np.empty_like(y)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        Ztr, Zte = standardize(X[tr], X[te])
        m = ElasticNetCV(l1_ratio=[0.1, 0.5, 0.9], alphas=30, cv=5, max_iter=5000,
                         random_state=seed, n_jobs=-1).fit(Ztr, y[tr])
        pred[te] = m.predict(Zte)
    return 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)


def cv_rrr(X, Y, rank, folds=10, seed=0):
    """Reduced-rank ridge: ridge fit, then project coefficients onto the top
    `rank` right singular vectors of the fitted training values."""
    X, Y = np.asarray(X, float), np.asarray(Y, float)
    pred = np.empty_like(Y)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        Ztr, Zte = standardize(X[tr], X[te])
        ym, ys = Y[tr].mean(0), Y[tr].std(0)
        ys[ys == 0] = 1.0
        Ytr = (Y[tr] - ym) / ys
        m = RidgeCV(alphas=ALPHAS).fit(Ztr, Ytr)
        fitted = m.predict(Ztr)
        _, _, Vt = np.linalg.svd(fitted - fitted.mean(0), full_matrices=False)
        P = Vt[:rank].T @ Vt[:rank]
        pred[te] = ((m.predict(Zte) - m.intercept_) @ P + m.intercept_) * ys + ym
    return 1 - ((Y - pred) ** 2).sum(0) / ((Y - Y.mean(0)) ** 2).sum(0)


# 1. elastic net, per feature
rows = []
for f in ephys.columns:
    X, y, g = feature_frame(expr, meta, ephys, f)
    raw = cv_enet(X, y)
    Xd, yd = demean(X, y, g)
    wt = cv_enet(Xd, yd)
    rows.append(dict(feature=f, n=len(y), enet_raw=raw, enet_within=wt))
    print(f"{f:40s} enet raw {raw:.3f} within {wt:.4f}", flush=True)
en = pd.DataFrame(rows)
en.to_csv(os.path.join(RES, "m1_elasticnet.csv"), index=False)
print("elastic net mean raw", en.enet_raw.mean(), "within", en.enet_within.mean())

# 2. reduced-rank ridge, all features jointly on cells with every feature present
Y = ephys.dropna()
g = meta.loc[Y.index, "RNA type"]
keep = filter_groups(g)
Y, g = Y.loc[keep], g.loc[keep]
X = expr.loc[Y.index]
Xd = X - X.groupby(g).transform("mean")
Yd = Y - Y.groupby(g).transform("mean")
out = pd.DataFrame({"feature": Y.columns})
for r in (2, 5):
    out[f"rrr{r}_raw"] = cv_rrr(X, Y, r)
    out[f"rrr{r}_within"] = cv_rrr(Xd, Yd, r)
out["n_cells"] = len(Y)
out["n_types"] = g.nunique()
out.to_csv(os.path.join(RES, "m1_reduced_rank.csv"), index=False)
print("cells", len(Y), "types", g.nunique())
print(out.drop(columns=["feature"]).mean())
print("rank2 within <= 0:", int((out.rrr2_within <= 0).sum()), "of", len(out))
