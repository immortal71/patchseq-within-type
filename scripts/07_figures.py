"""Figures for the full article, from results/*.csv. Light theme, print sizes (PNG 300 dpi + PDF)."""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = "results"
F = "figures"
os.makedirs(F, exist_ok=True)
RAW, WITHIN, NULL, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#a6a49d", "#0b0b0b", "#52514e", "#e4e2db"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 150, "font.family": "DejaVu Sans"})


def save(fig, name):
    fig.savefig(f"{F}/{name}.png", dpi=300, bbox_inches="tight")
    fig.savefig(f"{F}/{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def short(s):
    return s.replace(" (ms)", "").replace(" (mV)", "").replace(" (MOhm)", "").replace(" (pA)", "") \
            .replace(" (mV*s)", "").replace(" (s)", "")


# ---- Figure 1: raw vs within-type R^2 per feature, same cells ----
b = pd.read_csv(f"{R}/m1_baseline.csv")
p = pd.read_csv(f"{R}/m1_permutation.csv").set_index("feature")
b = b.set_index("feature").join(p[["p", "q_bh", "within_family"]])
b = b.sort_values("raw_sub")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 5.2), gridspec_kw=dict(width_ratios=[1.25, 1]))
y = np.arange(len(b))
a1.barh(y - 0.2, b.raw_sub, height=0.38, color=RAW, label="Across types (raw)")
a1.barh(y + 0.2, b.within, height=0.38, color=WITHIN, label="Within type")
a1.set_yticks(y, [short(s) for s in b.index])
a1.axvline(0, color=MUTED, lw=0.6)
a1.set_xlabel("Cross-validated R²")
a1.grid(axis="x", color=GRID, lw=0.5)
a1.legend(frameon=False, loc="lower right")
a1.set_title("a  Same cells, two questions", loc="left", fontsize=9, color=INK)
a2.scatter(b.raw_sub, b.within, s=22, color=WITHIN, edgecolor="white", lw=0.6, zorder=3)
sig = b[b.p < 0.05]
a2.scatter(sig.raw_sub, sig.within, s=46, facecolor="none", edgecolor=INK, lw=0.8, zorder=4,
           label="Beats within-type permutation null (p < 0.05)")
for name, r in b.sort_values("raw_sub").tail(4).iterrows():
    a2.annotate(short(name), (r.raw_sub, r.within), xytext=(-7, -2), textcoords="offset points",
                fontsize=6.5, color=MUTED, ha="right", va="center")
a2.axhline(0, color=MUTED, lw=0.6)
a2.set_xlabel("Raw R²")
a2.set_ylabel("Within-type R²")
a2.grid(color=GRID, lw=0.5)
a2.legend(frameon=False, loc="lower right", fontsize=6.5)
a2.set_title("b  Raw accuracy ranks features but not effect size", loc="left", fontsize=9, color=INK)
fig.tight_layout()
save(fig, "fig1_raw_vs_within")

# ---- Figure 2: calibration of within-type R^2 ----
cc = pd.read_csv(f"{R}/m1_calibration_curves.csv")
cal = pd.read_csv(f"{R}/m1_calibration.csv").set_index("feature")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1, 1.2]))
avg = cc.groupby("true").agg(mean=("mean", "mean"), lo=("lo", "mean"), hi=("hi", "mean"))
a1.fill_between(avg.index, avg.lo, avg.hi, color=RAW, alpha=0.15, lw=0)
a1.plot(avg.index, avg["mean"], color=RAW, marker="o", ms=3, lw=1.5, label="Recovered (mean, 10-90%)")
a1.plot([0, 0.4], [0, 0.4], color=NULL, lw=0.8, ls="--", label="Perfect recovery")
a1.set_xlabel("Planted within-type R²")
a1.set_ylabel("Recovered CV R²")
a1.legend(frameon=False, fontsize=6.5, loc="upper left")
a1.grid(color=GRID, lw=0.4)
a1.set_title("a  Weak effects are strongly attenuated", loc="left", fontsize=9)
cal = cal.sort_values("raw_same_cells")
yy = np.arange(len(cal))
a2.scatter(cal.raw_same_cells, yy, color=RAW, s=22, zorder=3, label="Raw R², same cells")
a2.errorbar(cal.implied_true, yy, xerr=[cal.implied_true - cal.implied_lo, cal.implied_hi - cal.implied_true],
            fmt="o", color=WITHIN, ms=4, lw=1.2, capsize=0, zorder=3, label="Implied true within-type R²")
a2.scatter(cal.observed_within, yy, marker="|", s=60, color=INK, zorder=4, label="Observed within-type R²")
a2.set_yticks(yy, [short(s) for s in cal.index])
a2.axvline(0, color=MUTED, lw=0.6)
a2.set_xlabel("R²")
a2.grid(axis="x", color=GRID, lw=0.4)
a2.legend(frameon=False, fontsize=6.2, loc="lower right")
a2.set_title("b  Corrected within-type effect vs raw", loc="left", fontsize=9)
fig.tight_layout()
save(fig, "fig2_calibration")

# ---- Figure 3: fitted Hodgkin-Huxley parameters ----
hh = pd.read_csv(f"{R}/m1_hh.csv").set_index("parameter").sort_values("raw_type_cells")
fig, ax = plt.subplots(figsize=(7.2, 2.8))
yy = np.arange(len(hh))
ax.barh(yy - 0.27, hh.raw_type_cells, height=0.26, color=RAW, label="Raw (same cells)")
ax.barh(yy, hh.within_family, height=0.26, color=NULL, label="Within family")
ax.barh(yy + 0.27, hh.within_type, height=0.26, color=WITHIN, label="Within type")
ax.set_yticks(yy, hh.index)
ax.axvline(0, color=MUTED, lw=0.6)
ax.set_xlabel("Cross-validated R²")
ax.grid(axis="x", color=GRID, lw=0.4)
ax.legend(frameon=False, fontsize=6.5, loc="lower right")
fig.tight_layout()
save(fig, "fig3_hh_parameters")

# ---- Figure 4: robustness of the residual to labels and gene set ----
lg = pd.read_csv(f"{R}/m1_labels_genesets.csv")
cols = [("within_published_type", "Published types"), ("within_kmeans30", "Non-channel clusters, k=30"),
        ("within_kmeans50", "Non-channel clusters, k=50"), ("within_hgnc", "HGNC gene set")]
fam = p["within_family"].reindex(lg.feature).values
vals = [fam] + [lg[c].values for c, _ in cols][1:3] + [lg["within_published_type"].values, lg["within_hgnc"].values]
labels = ["Family means (coarsest)", "Non-channel clusters, k=30", "Non-channel clusters, k=50", "Published types", "Published types, HGNC genes"]
fig, ax = plt.subplots(figsize=(7.2, 2.6))
ax.boxplot(vals, vert=False, widths=0.5, showfliers=True,
           medianprops=dict(color=WITHIN, lw=1.5), boxprops=dict(color=MUTED),
           whiskerprops=dict(color=MUTED), capprops=dict(color=MUTED),
           flierprops=dict(marker="o", ms=2.5, markerfacecolor=MUTED, markeredgecolor="none"))
ax.set_yticks(range(1, len(labels) + 1), labels)
ax.axvline(0, color=MUTED, lw=0.6)
ax.set_xlabel("Within-group CV R² across 29 features")
ax.grid(axis="x", color=GRID, lw=0.4)
fig.tight_layout()
save(fig, "fig4_partitions")

# ---- Figure 5: Hcn test ----
h = pd.read_csv(f"{R}/m1_hcn.csv").set_index("feature")
fig, ax = plt.subplots(figsize=(7.2, 2.6))
yy = np.arange(len(h))
ax.barh(yy, h.hcn_r2, height=0.5, color=WITHIN, label="Hcn1-4, within type")
ax.scatter(h.null_95, yy, marker="|", s=120, color=INK, label="95th pct, random 4-gene sets")
ax.scatter(h.hcn1_only, yy, marker="o", s=14, color=RAW, zorder=3, label="Hcn1 alone")
for i, (name, r) in enumerate(h.iterrows()):
    ax.text(max(r.hcn_r2, r.null_95, r.hcn1_only) + 0.0015, i, f"p={r.p:.3f}", va="center", fontsize=6.5, color=MUTED)
ax.set_yticks(yy, [short(s) for s in h.index])
ax.axvline(0, color=MUTED, lw=0.6)
ax.set_xlabel("Within-type CV R²")
ax.legend(frameon=False, fontsize=6.5, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3)
ax.grid(axis="x", color=GRID, lw=0.4)
fig.tight_layout()
save(fig, "fig5_hcn")
print("figures written to", F)
