# Ion channel expression mostly predicts neuronal cell identity, and only weakly predicts electrophysiology within a cell type

Aashish Kharel

Independent researcher, Kathmandu, Nepal. ORCID 0009-0001-1785-8228. Correspondence: aashishkharel7@gmail.com

## Abstract

Patch-seq datasets pair each neuron's transcriptome with its electrophysiology, and several studies report that ion channel gene expression predicts electrophysiological features with high cross-validated accuracy. Here I ask how much of that accuracy reflects a relationship within a transcriptomic cell type rather than differences between types. In 1,328 mouse motor cortex neurons, ridge regression on 390 channel genes reproduces published accuracy (R² up to 0.68). On the same cells, removing type means from both expression and target reduces mean R² across 29 features from 0.270 to 0.0024. A within-type residual survives a permutation null for 12 features (7 after false discovery correction), largest for the number of action potentials, input resistance and membrane time constant; resting membrane potential shows none (p = 0.76). Because cross-validated R² strongly underestimates weak effects at this sample size, I calibrated it against planted effects of known size. The implied true within-type R² for the best-predicted features is about 0.05 to 0.10, about four to fourteen times below raw accuracy, and below 0.05 for resting potential. For 13 Hodgkin-Huxley parameters fitted to the same cells in previous work, within-type and within-family R² are indistinguishable from zero, so family-level prediction reflects family means. Results hold with a second, curated channel gene list. Raw accuracy in this setting mostly measures how separable cell types are. Larger datasets should improve within-type prediction, but toward a ceiling several times below current raw figures.

Keywords: Patch-seq, ion channels, electrophysiology, cell types, cross-validation, effect size

## Introduction

Patch-seq records a neuron's electrophysiology and sequences its RNA from the same cell (Cadwell et al. 2016; Fuzik et al. 2016; Lipovsek et al. 2021), which makes it possible to ask directly how much a neuron's ion channel expression tells us about how it fires. Several analyses report that gene expression, and channel expression in particular, predicts electrophysiological features with substantial accuracy (Tripathy et al. 2017; Gouwens et al. 2020; Bernaerts et al. 2025).

Bernaerts et al. (2025) moved this question a step closer to mechanism. They fitted conductance-based Hodgkin-Huxley models to 955 mouse motor cortex neurons by simulation-based inference and predicted the fitted parameters from ion channel and marker gene expression with sparse reduced-rank regression. Prediction worked well across neuronal families and degraded across finer transcriptomic types. They attributed the degradation to limited dataset size, continuous variation within families and transcriptomic noise, and concluded that much larger datasets may be needed. A commentary in the same issue repeated that reading (Huang et al. 2025).

Older work points to a different explanation. In identified crustacean neurons, channel mRNA and current vary two- to fourfold between animals while firing stays similar (Schulz et al. 2006), and many different conductance combinations can produce the same behaviour (Prinz et al. 2004; Marder & Goaillard 2006; Goaillard & Marder 2021). In mouse motor cortex itself, Scala et al. (2021) found that types within a family are poorly separated in electrophysiological space. Bomkamp et al. (2019) showed that many gene to property correlations across cell types are driven by the split between excitatory and inhibitory classes, and that only some of them carry over to variation within a type. If within-type variation in channel expression carries little information about within-type variation in physiology, the accuracy reported across all cells comes mostly from identifying the cell type, and more data can only recover a within-type relationship of whatever size actually exists.

Telling these accounts apart needs a control that removes cell identity, and an estimate of how well that control could detect a real within-type effect at the available sample size. The control removes type means from both the expression matrix and the target, then refits the same model. The estimate comes from calibrating observed within-type accuracy against planted effects of known size, which turns a near-zero result into a bounded effect size.

The analysis relies on the count matrices, features, type labels, model code and per-cell fitted parameters that the original authors released. The dataset and the main papers discussed here share authors, so this paper questions one group's interpretation rather than a broad literature, and it uses that group's data and methods throughout.

Here I apply the control to 29 electrophysiological features and 13 fitted Hodgkin-Huxley parameters from mouse motor cortex, test it against within-type permutation nulls, calibrate it against planted effects, and repeat it with a second gene list and with cell groups defined without any channel gene. Mean cross-validated R² falls from 0.270 to 0.0024 once type means are removed, the calibrated within-type effect for the best-predicted features is about R² 0.05 to 0.10, and resting membrane potential and the fitted model parameters show no within-type relationship.

## Results

### Channel expression predicts electrophysiology well across all cells

Using 390 channel genes and the 29 released electrophysiological features of 1,304 to 1,328 motor cortex neurons, cross-validated ridge regression reproduces the published pattern (mean R² 0.244 across features). Action potential waveform and firing features are predicted best: upstroke-to-downstroke ratio 0.681, maximum number of action potentials 0.665, action potential width 0.646 and afterhyperpolarization 0.536. Input resistance reaches 0.424 and resting membrane potential 0.117. These values agree with the preprint version of this analysis to within 0.03 for every feature named here.

### Almost all of that accuracy is lost within transcriptomic type

Restricting to the 28 types with at least 15 cells (946 to 969 cells) and fitting on exactly those cells, raw R² averages 0.270. After the type mean is removed from expression and from the target, the same model reaches a mean R² of 0.0024 (Figure 1a). Upstroke-to-downstroke ratio falls from 0.736 to 0.003, action potential width from 0.713 to 0.013 and maximum number of action potentials from 0.706 to 0.022. Estimating type means inside each training fold, which removes any leakage between test cells and their groupmates, gives a mean of 0.0019, with the same features largest.

Raw accuracy still ranks features sensibly. Across the 29 features, raw and within-type R² are correlated (Spearman ρ = 0.75, p < 0.0001; Figure 1b). The observed within-type values, however, are 30 to 250 times smaller than the raw values for the best predicted features.

The collapse is not specific to ridge regression. In the preprint version of this analysis, per-feature elastic net gave a mean within-type R² of -0.0012 and sparse reduced-rank regression (Kobak et al. 2021), the estimator class used by Bernaerts et al., gave -0.083 at rank 2, with all 29 features at or below zero.

The result does not depend on the gene list. With the 308 genes of the HGNC ion channel gene group (292 shared with the prefix set), raw R² averages 0.269 and within-type R² 0.0028.

### A small within-type signal survives for some features, and none for resting potential

Permuting the residual target within type 500 times gives a null for each feature. Twelve of 29 features exceed their null at p < 0.05, and seven survive Benjamini-Hochberg correction at q < 0.05 (Table 1): maximum number of action potentials (R² 0.022), latency at rheobase plus 20 pA (0.015), membrane time constant (0.015), input resistance (0.016), rebound (0.013), action potential width (0.013) and action potential amplitude (0.010). The residual is small and above zero.

Resting membrane potential shows no within-type signal (R² -0.005, p = 0.76).

### Cross-validated R² underestimates weak within-type effects, and correcting for that bounds them

Small observed values could reflect either a small effect or a weak instrument. To tell these apart, linear signals of known size were planted into within-type-permuted copies of the residual target, so that the planted signal was the only within-type signal present (Figure 2).

At this sample size the pipeline is weak. A planted effect of true R² 0.05 was recovered as about 0.004 on average and detected in 37 to 63% of repeats; an effect of 0.10 was recovered as about 0.02 and detected in 80 to 100% of repeats (mean 92%) across the ten features calibrated; an effect of 0.15 was detected in 93 to 100%. At this sample size, cross-validated R² recovers only a small fraction of a weak within-type effect.

Mapping each observed within-type R² onto its feature's calibration curve gives the implied true within-type R² (Table 1). For the features with a surviving residual it is 0.06 to 0.10, for example 0.089 (10th to 90th percentile range 0.058 to 0.152) for maximum number of action potentials, 0.098 (0.059 to 0.131) for input resistance and 0.088 (0.056 to 0.145) for action potential width. For upstroke-to-downstroke ratio it is 0.053 (0.010 to 0.114). For resting membrane potential it is 0, with an upper value of 0.05.

Compared with raw R² on the same cells, these corrected values are about 4 to 14 times smaller (3.8 to 13.8): 0.736 against 0.053 for upstroke-to-downstroke ratio, 0.706 against 0.089 for maximum number of action potentials, 0.477 against 0.098 for input resistance and 0.229 against 0.061 for sag ratio.

### The same pattern holds for fitted Hodgkin-Huxley parameters

Reproducing the preprocessing of Bernaerts et al. (2025) exactly (427 genes, 955 cells), raw R² for the 13 fitted parameters averages 0.173, and the ranking matches theirs: the steady-state ratio r_SS is predicted best (0.619), then the delayed-rectifier and Kv3.1 conductances (0.308 and 0.282) and membrane capacitance (0.277), with the muscarinic conductance and leak reversal potential worst (0.015 and 0.032). Within transcriptomic type (19 types with at least 15 cells, 668 cells), mean R² is -0.0045 and 12 of 13 parameters are at or below zero (Figure 3). Only the spike threshold parameter VT passes its permutation null (R² 0.008, p = 0.04), which is the number expected by chance among 13 tests.

Within family (7 families, 942 cells), mean R² is 0.002. The good family-level prediction of model parameters reported for this dataset comes from differences between family means. For the expert-defined electrophysiological features, by contrast, removing only family means leaves a mean R² of 0.036 (input resistance 0.090, membrane time constant 0.158), because transcriptomic types within a family still differ.

### Coarser identity partitions leave more residual

If the residual largely reflects cell identity, removing a coarser or noisier identity partition should leave more of it behind. That is what happens (Figure 4). Removing family means leaves a mean within-group R² of 0.036. Clustering cells on 3,000 variable non-channel genes, with every channel gene excluded, gives groups that agree only modestly with the published types (adjusted Rand index 0.21 for k = 30 and k = 50) and leaves 0.056 (k = 30) and 0.041 (k = 50). The published types leave 0.0024. This check does not rule out that some of the within-type collapse comes from types defined partly by channel genes. What it shows is that the size of the residual depends on how finely identity is removed.

### The Ih-linked residual depends on Hcn1

Hcn1 to Hcn4 together predict sag ratio within type above random four-gene channel sets (R² 0.0075, p = 0.018), as well as sag time (0.0074, p = 0.026); sag area is borderline (0.0039, p = 0.060). Rebound (p = 0.59), membrane time constant (p = 0.80), resting potential (p = 0.10) and action potential width (p = 0.06) are not significant. Dropping Hcn1 removes the effect for all three sag measures (sag ratio -0.0023), while Hcn1 alone does slightly better than the four genes together (0.012 for sag ratio). These numbers reproduce the preprint. Because Hcn1 was singled out after the four-gene test, and the effect is small, this remains suggestive.

**Table 1. Raw and within-type prediction of 29 electrophysiological features from 390 channel genes (mouse motor cortex).** Values are cross-validated R². "Raw, all": all cells with the feature. "Raw, same", "Within" and "Within, fold-wise" use the 946 to 969 cells in the 28 types with at least 15 cells. P values from 500 within-type permutations (smallest attainable 0.002). Implied true R² from the calibration in Figure 2, given for the ten calibrated features.

| Feature | Raw, all | Raw, same | Within | Within, fold-wise | p | q | Implied true within (range) |
|---|---|---|---|---|---|---|---|
| Upstroke-to-downstroke ratio | 0.681 | 0.736 | 0.0028 | 0.0023 | 0.050 | 0.121 | 0.053 (0.010 to 0.114) |
| AP width (ms) | 0.646 | 0.713 | 0.0129 | 0.0101 | 0.006 | 0.039 | 0.088 (0.056 to 0.145) |
| Max number of APs | 0.665 | 0.706 | 0.0221 | 0.0176 | 0.002 | 0.029 | 0.089 (0.058 to 0.152) |
| Afterhyperpolarization (mV) | 0.536 | 0.589 | 0.0057 | 0.0041 | 0.020 | 0.064 |  |
| AP amplitude (mV) | 0.425 | 0.482 | 0.0098 | 0.0114 | 0.008 | 0.039 | 0.061 (0.023 to 0.115) |
| Input resistance (MOhm) | 0.424 | 0.477 | 0.0161 | 0.0093 | 0.012 | 0.050 | 0.098 (0.059 to 0.131) |
| Rebound (mV) | 0.301 | 0.382 | 0.0130 | 0.0131 | 0.008 | 0.039 | 0.081 (0.035 to 0.143) |
| Membrane time constant (ms) | 0.320 | 0.376 | 0.0150 | 0.0128 | 0.004 | 0.039 | 0.085 (0.057 to 0.139) |
| Latency @ +20pA current (ms) | 0.286 | 0.325 | 0.0152 | 0.0137 | 0.002 | 0.029 | 0.081 (0.053 to 0.118) |
| AP amplitude adaptation index | 0.283 | 0.321 | -0.0027 | -0.0018 | 0.295 | 0.476 |  |
| Burstiness | 0.311 | 0.318 | 0.0001 | -0.0047 | 0.120 | 0.232 |  |
| Sag area (mV*s) | 0.279 | 0.306 | 0.0038 | -0.0005 | 0.030 | 0.087 |  |
| Rheobase (pA) | 0.294 | 0.304 | 0.0030 | 0.0027 | 0.040 | 0.105 |  |
| Sag time (s) | 0.255 | 0.281 | 0.0005 | -0.0014 | 0.088 | 0.196 |  |
| ISI coefficient of variation | 0.208 | 0.229 | -0.0040 | -0.0061 | 0.551 | 0.761 |  |
| Sag ratio | 0.196 | 0.229 | 0.0085 | 0.0069 | 0.020 | 0.064 | 0.061 (0.023 to 0.106) |
| Resting membrane potential (mV) | 0.117 | 0.152 | -0.0051 | -0.0038 | 0.758 | 0.782 | 0.000 (0.000 to 0.050) |
| Spike frequency adaptation | 0.173 | 0.150 | -0.0057 | -0.0013 | 0.776 | 0.782 |  |
| Rebound number of APs | 0.142 | 0.150 | -0.0050 | -0.0052 | 0.655 | 0.782 |  |
| Afterdepolarization (mV) | 0.071 | 0.110 | -0.0049 | -0.0038 | 0.729 | 0.782 |  |
| ISI adaptation index | 0.097 | 0.102 | -0.0019 | -0.0011 | 0.132 | 0.239 |  |
| Wildness | 0.087 | 0.080 | -0.0050 | -0.0054 | 0.639 | 0.782 |  |
| ISI Fano factor | 0.045 | 0.079 | -0.0053 | -0.0046 | 0.745 | 0.782 |  |
| AP amplitude average adaptation index | 0.044 | 0.076 | -0.0025 | -0.0020 | 0.279 | 0.476 |  |
| ISI average adaptation index | 0.080 | 0.063 | -0.0030 | -0.0014 | 0.433 | 0.661 |  |
| AP threshold (mV) | 0.056 | 0.053 | -0.0042 | -0.0003 | 0.641 | 0.782 |  |
| Latency (ms) | 0.035 | 0.037 | -0.0006 | -0.0001 | 0.100 | 0.207 |  |
| AP Fano factor | 0.022 | 0.010 | -0.0035 | -0.0022 | 0.495 | 0.718 |  |
| AP coefficient of variation | 0.007 | 0.004 | -0.0051 | -0.0027 | 0.782 | 0.782 |  |

## Discussion

Across all cells, ion channel expression predicts many electrophysiological features well. Within a transcriptomic type, it predicts very little, and what it does predict is far smaller than the raw figures suggest. After correcting cross-validated R² for the attenuation that affects weak effects at this sample size, the within-type relationship for the best-predicted features is around R² 0.05 to 0.10, four to fourteen times below the raw accuracy on the same cells. For resting membrane potential, there is no detectable within-type relationship at all.

### What raw accuracy measures

The simplest reading is that a regression from channel expression to physiology combines two real relationships: channel expression identifies cell type, and cell type largely determines physiology. Voltage-gated channel genes are good type markers, so a model can score highly across cells while learning mostly which type a cell belongs to. Raw accuracy still ranks features in roughly the right order of within-type signal (ρ = 0.75). It should not be read as the strength of a gene-to-function link inside a cell type, and claims of that kind need a within-type figure alongside the raw one.

This fits older evidence that cells of one type reach similar behaviour with different channel complements (Schulz et al. 2006; Marder & Goaillard 2006; Goaillard & Marder 2021), the finding that many cross-type gene to property correlations are class-driven (Bomkamp et al. 2019), and the observation from this same dataset that types within a family are poorly separated electrophysiologically (Scala et al. 2021). Transcript abundance also captures only one factor of membrane conductance. Conductance depends on channel number, open probability and single-channel conductance, and the mRNA count is a noisy proxy for the first of these only. Trafficking, subunit composition and modulation are invisible to it.

### Data size, revisited

Bernaerts et al. (2025) attributed the loss of accuracy at the level of fine types to limited data. The preprint version of this paper argued the opposite, that the within-type quantity is too small for more data to matter. The power analysis here shows that argument went too far. At roughly 950 cells and 390 genes, a within-type effect of R² 0.05 is detected only about half the time, so the near-zero observed values are consistent with real effects of that size, and more cells would recover more of them.

What the analysis does support is a ceiling. For most features with a surviving residual, the implied true within-type R² is at or below about 0.15 even at the upper end of its range, and for resting membrane potential it is below about 0.05. Larger datasets should improve within-type prediction, and the value they approach is several times smaller than current raw figures. The two accounts, insufficient data and a small target, are both partly right, and the useful quantity for planning future datasets is the size of that target.

For fitted Hodgkin-Huxley parameters, within-type and within-family R² are indistinguishable from zero, and family-level prediction is carried by family means. The mechanistic interpretability of a model parameter does not by itself establish that its gene-to-parameter mapping holds within a cell type.

### The resting potential null and the Ih exception

Resting potential is set by small leak currents near equilibrium, pump activity and intracellular ion concentrations, none of which channel transcript counts capture. This matters for attempts to infer resting potential from channel expression, including in tissues outside the nervous system. Within a cell type, this dataset gives no support for that inference.

The sag-related residual traces mainly to Hcn1. HCN channels have small single-channel conductance but are numerous and partly open near rest, so Ih may scale with channel number more directly than most currents. The model of Bernaerts et al. contains no hyperpolarization-activated current and was fitted to depolarizing steps, so it could not represent this effect even if present. The Hcn1 result was found after a four-gene test and is small; it needs replication in an independent dataset with hyperpolarizing protocols.

### Scope

The same decomposition applies to any method that infers a functional quantity from expression of the genes that implement it, such as metabolic flux, transcription factor activity or ligand-receptor communication, wherever cell types differ in both expression and function. Reporting a within-type control, with an estimate of how much a weak within-type effect would be attenuated at the available sample size, would make such claims easier to interpret.

### Limitations

All results come from one dataset, one brain region and one species. A script to repeat the main analysis on the larger mouse visual cortex Patch-seq release is provided but could not be run here because its count matrix was not reachable from the analysis environment. Transcriptomic types are defined from the transcriptome, partly including channel genes. Clusters built without any channel gene agreed only modestly with the published types and left more residual, so this check cannot exclude some circularity. The calibration assumes a linear, dense or sparse signal over the same genes; a nonlinear relationship could be recovered differently. Fitted model parameters are point estimates from a degenerate posterior, which attenuates raw and residual estimates alike. The elastic net and sRRR comparisons are carried over from the preprint rather than rerun. A learning curve was attempted and is not reported. Subsampling cells shrinks every type, and with fewer than about 10 cells per type both ways of removing type means are biased, in opposite directions, so the curve could not separate effect size from estimation error.

## Methods

### Data

Mouse primary motor cortex Patch-seq data (Scala et al. 2021) were taken from the public mini-atlas repository (github.com/berenslab/mini-atlas): exon and intron count matrices, 29 electrophysiological features, cell metadata including transcriptomic family and type, and gene lengths. Fitted Hodgkin-Huxley parameters (maximum a posteriori sample per cell, 13 parameters) were taken from the hh_sbi repository (github.com/berenslab/hh_sbi) released with Bernaerts et al. (2025). No new animal or human data were generated, so no ethics approval was required.

### Expression preprocessing

Exon and intron counts were summed per gene, converted to reads per kilobase per million (library size over all genes, length from the released gene_bp column) and transformed with log(1 + x). Channel genes were selected by prefix over standard channel families (potassium, sodium, calcium and chloride channels; HCN; TRP; connexins and pannexins; anoctamins and bestrophins; acid-sensing; P2X; ionotropic GABA, glycine, glutamate, nicotinic and 5-HT3 receptors; ryanodine and IP3 receptors; Piezo; LRRC8; tweety; NALCN; Orai; CatSper; TPC; Hv1; CLIC; ZAC; polycystin-2; mucolipin; CNG; CFTR; TMC; otopetrin; CALHM). Genes detected in fewer than 10 cells were removed, a filter that does not use labels or targets. This left 390 genes. As a robustness check, the HGNC ion channel gene group shipped with the mini-atlas repository was used instead (human symbols mapped to mouse by case).

### Regression

Each feature was predicted with ridge regression under 10-fold cross-validation. Inside each training fold, predictors were standardized with training-fold statistics and the penalty was chosen by generalized cross-validation over 30 log-spaced values from 0.01 to 100,000. Test-fold standardized values were clipped to the range seen in the training fold; without this, a gene that is almost constant in one training fold produced extreme predictions for single test cells. R² was computed once on the pooled held-out predictions against the total sum of squares. Elastic net and sparse reduced-rank regression (sRRR) results are taken from the preprint version of this work and are labelled as such.

### Within-group control

Cells were grouped by transcriptomic type; types with fewer than 15 cells for a given feature were dropped (28 types, 946 to 969 cells depending on the feature; 1,304 to 1,328 cells in the raw analysis on all cells). The type mean was subtracted from every predictor column and from the target, and cross-validation was run on the residuals exactly as on raw data. Subtracting means computed on all cells lets each test cell contribute to the mean removed from its training-fold groupmates, which can leak signal when groups are small. All within-type results were also computed with type means estimated inside each training fold and subtracted from both training and test cells; the two estimators give the same conclusions (fold-wise mean across features 0.0019, against 0.0024). Raw R² is reported both on all cells with the feature and on the identical cells used for the within-type fit; the second comparison is the one used for ratios. The same procedure was applied with transcriptomic family in place of type.

### Permutation null

For each feature, the within-type residual target was permuted inside each type 500 times and refit with identical cross-validation. Because the predictor matrix is fixed, all permutations were fit jointly with one decomposition per fold and the penalty chosen per target. P values are (1 + number of permutations at or above the observed R²) / 501. Benjamini-Hochberg correction (Benjamini & Hochberg 1995) was applied across the 29 features.

### Fitted Hodgkin-Huxley parameters

For the 13 fitted parameters, the preprocessing of Bernaerts et al. (2025) was reproduced: their Gene Ontology ion channel list (matched by symbol) plus Pvalb, Lamp5, Vip and Sst; exon counts only; genes with at least 10 total counts; counts scaled to the median of the selected genes' library size; log2(x + 1). This gave 427 genes and 955 cells. The maximum a posteriori parameters are the highest-evaluation posterior sample per cell from their preferred training schedule. Raw, within-type (19 types with at least 15 cells, 668 cells) and within-family (7 families, 942 cells) R² and a 200-permutation within-type null were computed as above, fitting all parameters jointly.

### Power and calibration

For each of ten features (the seven passing correction, upstroke-to-downstroke ratio, sag ratio and resting membrane potential), the within-type residual target was first permuted within type, which removes any real within-type signal while keeping its distribution. A linear signal built from the real within-type residual expression, with independent normal weights on every gene, was then added and scaled to a known share of the total variance (true R² of 0.02, 0.05, 0.10, 0.15, 0.20, 0.30 or 0.40; 30 repeats each). Each planted target was scored with the same cross-validated ridge as the real data. A planted signal counted as detected when its R² exceeded the 95th percentile of the feature's within-type permutation null (200 permutations). The mean recovered R² at each level, with the true R² = 0 point taken as the null median, forms a calibration curve; the observed within-type R² was mapped onto it by linear interpolation to give an implied true R², and onto the curves of the 90th and 10th percentiles of recovered R² to give a range. An earlier version with dense and sparse (five-gene) signals at 0.005 to 0.10 gave the same picture for sparse signals.

### Label-independent groups

To check that the result does not depend on labels derived from the tested genes, every channel gene (by prefix or HGNC membership) was removed, the 3,000 most variable remaining genes (log counts per million) were reduced to 50 principal components, and cells were clustered by k-means with k = 30 and k = 50. The within-group control was then repeated with these clusters.

### HCN test

Within type, Hcn1 to Hcn4 were used as the only predictors for seven features and compared with 500 random sets of four other channel genes. Leave-one-gene-out and Hcn1-only fits were also run. The four-gene test and its features were specified in the preprint before it was first run.

### Visual cortex replication

A script that applies the same pipeline to the mouse visual cortex Patch-seq release (Gouwens et al. 2020; 23 features as extracted by Bernaerts et al. 2025) is provided. That release contains exon counts without gene lengths, so expression is log(1 + counts per million).

### Software and availability

Python 3 with NumPy, pandas and scikit-learn 1.9. All scripts download or read only public inputs and are available at https://github.com/immortal71/patchseq-within-type.

### Use of AI tools

An AI assistant (Claude, Anthropic) was used to write and debug analysis code, run analyses, check references against PubMed, draft and edit text, and make figures. The author directed the research question and analysis plan, reviewed every result and all text, and takes full responsibility for the content.

## Figure legends

**Figure 1. Channel expression predicts electrophysiology across cell types but barely within them.** (a) Cross-validated ridge R² for 29 features from 390 channel genes, on the 946 to 969 cells in the 28 transcriptomic types with at least 15 cells. Blue: raw. Orange: after removing type means from expression and target. (b) Raw against within-type R² per feature. Circled points beat their within-type permutation null (500 permutations, p < 0.05). Note the different axis scales.

**Figure 2. Calibrating within-type R² against planted effects.** (a) Linear signals of known size were added to within-type-permuted residual targets and scored with the same pipeline (30 repeats per level, averaged over ten features; band shows the mean 10th to 90th percentile). Weak effects are recovered at a small fraction of their true size. (b) For each calibrated feature: raw R² on the same cells (blue), observed within-type R² (black tick) and the implied true within-type R² with its range (orange).

**Figure 3. Fitted Hodgkin-Huxley parameters.** Cross-validated R² for the 13 maximum a posteriori parameters of Bernaerts et al. (2025), predicted from their 427-gene set. Raw on the 668 cells of the 19 types with at least 15 cells (blue), after removing family means (grey; 942 cells, 7 families) and after removing type means (orange).

**Figure 4. How much residual survives depends on how finely identity is removed.** Distribution across the 29 features of within-group R² after removing means of transcriptomic families, of k-means clusters built from non-channel genes only (k = 30 and 50), of published transcriptomic types, and of published types with the HGNC channel gene list.

**Figure 5. HCN genes and sag within type.** Within-type R² using Hcn1 to Hcn4 as the only predictors (orange bars), Hcn1 alone (blue dots), and the 95th percentile of 500 random four-gene channel sets (black ticks), with permutation p values.

## Data and code availability

All input data are public: github.com/berenslab/mini-atlas (Scala et al. 2021) and github.com/berenslab/hh_sbi (Bernaerts et al. 2025). Every analysis script, result table and figure script is available at https://github.com/immortal71/patchseq-within-type under the MIT licence. The visual cortex replication script requires the Allen Institute mouse visual cortex Patch-seq release (Gouwens et al. 2020).

## Funding

This research received no external funding.

## Acknowledgements

I thank the authors of Scala et al. (2021) and Bernaerts et al. (2025) for releasing their data, code and fitted parameters in full, which made this analysis possible.

## Conflicts of interest

The author declares no conflicts of interest.

## References

Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J R Stat Soc Ser B. 1995;57(1):289-300. doi:10.1111/j.2517-6161.1995.tb02031.x

Bernaerts Y, Deistler M, Gonçalves PJ, Beck J, Stimberg M, Scala F, Tolias AS, Macke JH, Kobak D, Berens P. Combined statistical-biophysical modeling links ion channel genes to physiology of cortical neuron types. Patterns. 2025;6(10):101323. doi:10.1016/j.patter.2025.101323

Bomkamp C, Tripathy SJ, Bengtsson Gonzales C, Hjerling-Leffler J, Craig AM, Pavlidis P. Transcriptomic correlates of electrophysiological and morphological diversity within and across excitatory and inhibitory neuron classes. PLoS Comput Biol. 2019;15(6):e1007113. doi:10.1371/journal.pcbi.1007113

Cadwell CR, Palasantza A, Jiang X, et al. Electrophysiological, transcriptomic and morphologic profiling of single neurons using Patch-seq. Nat Biotechnol. 2016;34(2):199-203. doi:10.1038/nbt.3445

Fuzik J, Zeisel A, Máté Z, et al. Integration of electrophysiological recordings with single-cell RNA-seq data identifies neuronal subtypes. Nat Biotechnol. 2016;34(2):175-183. doi:10.1038/nbt.3443

Goaillard JM, Marder E. Ion channel degeneracy, variability, and covariation in neuron and circuit resilience. Annu Rev Neurosci. 2021;44:335-357. doi:10.1146/annurev-neuro-092920-121538

Gouwens NW, Sorensen SA, Baftizadeh F, et al. Integrated morphoelectric and transcriptomic classification of cortical GABAergic cells. Cell. 2020;183(4):935-953.e19. doi:10.1016/j.cell.2020.09.057

Huang W, Xu Q, Liu S. Linking ion channel gene expression to neuronal firing patterns through a statistical-biophysical model. Patterns. 2025;6(10):101390. doi:10.1016/j.patter.2025.101390

Kobak D, Bernaerts Y, Weis MA, Scala F, Tolias AS, Berens P. Sparse reduced-rank regression for exploratory visualisation of paired multivariate data. J R Stat Soc Ser C Appl Stat. 2021;70(4):980-1000. doi:10.1111/rssc.12494

Lipovsek M, Bardy C, Cadwell CR, Hadley K, Kobak D, Tripathy SJ. Patch-seq: past, present, and future. J Neurosci. 2021;41(5):937-946. doi:10.1523/JNEUROSCI.1653-20.2020

Marder E, Goaillard JM. Variability, compensation and homeostasis in neuron and network function. Nat Rev Neurosci. 2006;7(7):563-574. doi:10.1038/nrn1949

Prinz AA, Bucher D, Marder E. Similar network activity from disparate circuit parameters. Nat Neurosci. 2004;7(12):1345-1352. doi:10.1038/nn1352

Scala F, Kobak D, Bernabucci M, et al. Phenotypic variation of transcriptomic cell types in mouse motor cortex. Nature. 2021;598(7879):144-150. doi:10.1038/s41586-020-2907-3

Schulz DJ, Goaillard JM, Marder E. Variable channel expression in identified single and electrically coupled neurons in different animals. Nat Neurosci. 2006;9(3):356-362. doi:10.1038/nn1639

Tripathy SJ, Toker L, Li B, et al. Transcriptomic correlates of neuron electrophysiological diversity. PLoS Comput Biol. 2017;13(10):e1005814. doi:10.1371/journal.pcbi.1005814
