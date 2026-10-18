"""Core pipeline for the within-type control on M1 Patch-seq (Scala et al. 2021).

Reproduces the preprint pipeline:
  exon + intron counts -> RPKM by gene length -> log1p, ion channel genes by prefix,
  10-fold CV ridge (alpha by GCV inside each training fold, predictors standardized
  inside each training fold), R^2 on pooled held-out predictions.
Within-type control: keep types with >= MIN_CELLS cells, subtract type means from
both X and y, refit exactly the same way.
"""
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold

DATA = "data/mini-atlas/data"
CACHE = "cache"
ALPHAS = np.logspace(-2, 5, 30)
MIN_CELLS = 15

# Standard channel gene families (mouse symbols). Prefix match, as in the preprint.
PREFIXES = (
    "Kcn", "Scn", "Cacn", "Clcn", "Hcn", "Trp", "Gja", "Gjb", "Gjc", "Gjd",
    "Ano", "Best", "Asic", "P2rx", "Gabr", "Glr", "Gria", "Grik", "Grin", "Grid",
    "Chrn", "Htr3", "Ryr", "Itpr", "Piezo", "Lrrc8", "Ttyh", "Nalcn", "Orai",
    "Catsper", "Tpcn", "Hvcn", "Clic", "Zacn", "Pkd2", "Mcoln", "Cnga", "Cngb",
    "Panx", "Cftr", "Tmc", "Otop", "Calhm",
)


def load_m1():
    """Return expression (cells x genes, log1p RPKM), meta, ephys, all aligned."""
    os.makedirs(CACHE, exist_ok=True)
    pq = os.path.join(CACHE, "m1_logrpkm_channels.pkl")
    meta = pd.read_csv(os.path.join(DATA, "m1_patchseq_meta_data.csv"), sep="\t").set_index("Cell")
    ephys = pd.read_csv(os.path.join(DATA, "m1_patchseq_ephys_features.csv")).set_index("cell id")
    if os.path.exists(pq):
        expr = pd.read_pickle(pq)
    else:
        ex = pd.read_csv(os.path.join(DATA, "m1_patchseq_exon_counts.csv.gz"), index_col=0)
        it = pd.read_csv(os.path.join(DATA, "m1_patchseq_intron_counts.csv.gz"), index_col=0)
        it = it.reindex(index=ex.index, columns=ex.columns).fillna(0)
        counts = ex + it
        gl = pd.read_csv(os.path.join(DATA, "gene_lengths.txt")).set_index("GeneID")["gene_bp"]
        genes = [g for g in counts.index if g.startswith(PREFIXES) and g in gl.index]
        lib = counts.sum(axis=0)  # library size over ALL genes
        sub = counts.loc[genes]
        rpkm = sub.div(gl.loc[genes] / 1e3, axis=0).div(lib / 1e6, axis=1)
        expr = np.log1p(rpkm).T
        # Keep genes detected in at least 10 cells (label-free filter).
        expr = expr.loc[:, (expr > 0).sum(axis=0) >= 10]
        expr.to_pickle(pq)
    cells = expr.index.intersection(ephys.index).intersection(meta.index)
    return expr.loc[cells], meta.loc[cells], ephys.loc[cells]


def cv_r2(X, y, folds=10, seed=0, return_pred=False):
    """10-fold CV ridge, GCV alpha inside each training fold, pooled held-out R^2."""
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    pred = np.empty_like(y)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd[sd == 0] = 1.0
        Ztr = (X[tr] - mu) / sd
        # Clip test z-scores to the training range so a gene that is near-constant in
        # the training fold cannot produce an extreme extrapolated prediction.
        Zte = np.clip((X[te] - mu) / sd, Ztr.min(0), Ztr.max(0))
        m = RidgeCV(alphas=ALPHAS).fit(Ztr, y[tr])
        pred[te] = np.asarray(m.predict(Zte)).ravel()
    r2 = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
    return (r2, pred) if return_pred else r2


def demean(X, y, groups):
    """Subtract group means from X and y (groups assumed already filtered)."""
    Xd = X - X.groupby(groups).transform("mean")
    yd = y - y.groupby(groups).transform("mean")
    return Xd, yd


def filter_groups(groups, min_cells=MIN_CELLS):
    vc = groups.value_counts()
    keep = vc[vc >= min_cells].index
    return groups.isin(keep) & groups.notna()


def feature_frame(expr, meta, ephys, feature, group_col="RNA type"):
    """Rows usable for one feature: non-missing target, group with >= MIN_CELLS cells."""
    y = ephys[feature]
    ok = y.notna() & meta[group_col].notna()
    g = meta.loc[ok, group_col]
    keep = filter_groups(g)
    idx = g.index[keep]
    return expr.loc[idx], y.loc[idx], meta.loc[idx, group_col]


def cv_r2_multi(X, Y, folds=10, seed=0):
    """Same as cv_r2 but for many targets at once (columns of Y), alpha chosen per target.

    Used for permutation nulls and simulations: X is fixed, only y changes, so one
    decomposition per fold serves every column.
    """
    X = np.asarray(X, float)
    Y = np.asarray(Y, float)
    pred = np.empty_like(Y)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd[sd == 0] = 1.0
        Ztr = (X[tr] - mu) / sd
        Zte = np.clip((X[te] - mu) / sd, Ztr.min(0), Ztr.max(0))
        m = RidgeCV(alphas=ALPHAS, alpha_per_target=True).fit(Ztr, Y[tr])
        pred[te] = np.asarray(m.predict(Zte)).reshape(len(te), -1)
    ss_res = ((Y - pred) ** 2).sum(0)
    ss_tot = ((Y - Y.mean(0)) ** 2).sum(0)
    return 1 - ss_res / ss_tot


def cv_r2_within(X, y, groups, folds=10, seed=0, Y_extra=None):
    """Within-group CV R^2 with group means estimated on the TRAINING fold only.

    Demeaning the whole dataset before CV lets a test cell's value enter its group
    mean, which its training-fold groupmates then carry; with small groups this
    leaks signal. Here, for every fold, group means of X and y come from training
    cells only and are subtracted from both training and test cells.
    If Y_extra (n x k) is given, those columns are scored the same way and returned.
    """
    X = np.asarray(X, float)
    Y = np.asarray(y, float).reshape(len(X), -1)
    if Y_extra is not None:
        Y = np.column_stack([Y, np.asarray(Y_extra, float)])
    g = np.asarray(groups)
    pred = np.full_like(Y, np.nan)
    resid = np.full_like(Y, np.nan)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        Xtr, Xte = X[tr].copy(), X[te].copy()
        Ytr, Yte = Y[tr].copy(), Y[te].copy()
        ok_te = np.ones(len(te), bool)
        for lab in np.unique(g[tr]):
            mtr = g[tr] == lab
            mte = g[te] == lab
            mx, my = Xtr[mtr].mean(0), Ytr[mtr].mean(0)
            Xtr[mtr] -= mx
            Ytr[mtr] -= my
            Xte[mte] -= mx
            Yte[mte] -= my
        ok_te &= np.isin(g[te], np.unique(g[tr]))
        mu, sd = Xtr.mean(0), Xtr.std(0)
        sd[sd == 0] = 1.0
        Ztr = (Xtr - mu) / sd
        Zte = np.clip((Xte - mu) / sd, Ztr.min(0), Ztr.max(0))
        m = RidgeCV(alphas=ALPHAS, alpha_per_target=True).fit(Ztr, Ytr)
        p = np.asarray(m.predict(Zte)).reshape(len(te), -1)
        pred[te[ok_te]] = p[ok_te]
        resid[te[ok_te]] = Yte[ok_te]
    ok = ~np.isnan(resid[:, 0])
    ss_res = ((resid[ok] - pred[ok]) ** 2).sum(0)
    ss_tot = ((resid[ok] - resid[ok].mean(0)) ** 2).sum(0)
    r2 = 1 - ss_res / ss_tot
    return r2 if Y.shape[1] > 1 else float(r2[0])
