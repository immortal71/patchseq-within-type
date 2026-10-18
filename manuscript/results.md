## Results

### Channel expression predicts electrophysiology well across all cells

Using 390 channel genes and the 29 released electrophysiological features of 1,304 to 1,328 motor cortex neurons, cross-validated ridge regression reproduces the published pattern (mean R² 0.244 across features). Action potential waveform and firing features are predicted best: upstroke-to-downstroke ratio 0.681, maximum number of action potentials 0.665, action potential width 0.646 and afterhyperpolarization 0.536. Input resistance reaches 0.424 and resting membrane potential 0.117.

### Almost all of that accuracy is lost within transcriptomic type

Restricting to the 28 types with at least 15 cells (946 to 969 cells) and fitting on exactly those cells, raw R² averages 0.270. After the type mean is removed from expression and from the target, the same model reaches a mean R² of 0.0024 (Figure 1a). Upstroke-to-downstroke ratio falls from 0.736 to 0.003, action potential width from 0.713 to 0.013 and maximum number of action potentials from 0.706 to 0.022. Estimating type means inside each training fold, which removes any leakage between test cells and their groupmates, gives a mean of 0.0019, with the same features largest.

Raw accuracy still ranks features sensibly. Across the 29 features, raw and within-type R² are correlated (Spearman ρ = 0.75, p < 0.0001; Figure 1b). The observed within-type values, however, are 30 to 250 times smaller than the raw values for the best predicted features.

The collapse is not specific to ridge regression. On the same cells and folds, per-feature elastic net reaches a mean raw R² of 0.273 and a mean within-type R² of 0.0008. Reduced-rank ridge regression, which predicts all 29 features jointly through a low-rank bottleneck like the sparse reduced-rank regression used by Bernaerts et al. (Kobak et al. 2021), was fitted on the 946 cells with every feature measured. It reaches mean raw R² of 0.237 at rank 2 and 0.263 at rank 5, and mean within-type R² of 0.0010 and 0.0016; at rank 2, 17 of 29 features are at or below zero.

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

Hcn1 to Hcn4 together predict sag ratio within type above random four-gene channel sets (R² 0.0075, p = 0.018; Figure 5), as well as sag time (0.0074, p = 0.026); sag area is borderline (0.0039, p = 0.060). Rebound (p = 0.59), membrane time constant (p = 0.80), resting potential (p = 0.10) and action potential width (p = 0.06) are not significant. Dropping Hcn1 removes the effect for all three sag measures (sag ratio -0.0023), while Hcn1 alone does slightly better than the four genes together (0.012 for sag ratio). Because Hcn1 was singled out after the four-gene test, and the effect is small, this remains suggestive.
