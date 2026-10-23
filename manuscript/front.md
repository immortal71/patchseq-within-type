# Ion channel expression mostly predicts neuronal cell identity, and only weakly predicts electrophysiology within a cell type

Aashish Kharel

Independent researcher, Kathmandu, Nepal. ORCID 0009-0001-1785-8228. Correspondence: aashishkharel7@gmail.com

## Abstract

Patch-seq datasets pair each neuron's transcriptome with its electrophysiology, and several studies report that ion channel gene expression predicts electrophysiological features with high cross-validated accuracy. Here I ask how much of that accuracy reflects a relationship within a transcriptomic cell type rather than differences between types. In 1,328 mouse motor cortex neurons, ridge regression on 390 channel genes gives accuracy close to published reports (R² up to 0.68). On the same cells, removing type means from both expression and target reduces mean R² across 29 features from 0.270 to 0.0024. A within-type residual survives a permutation null for 12 features (7 after false discovery correction), largest for the maximum number of action potentials, input resistance and spike latency; resting membrane potential shows none (p = 0.76). Because cross-validated R² strongly underestimates weak effects at this sample size, I calibrated it against planted effects of known size. The implied true within-type R² for the best-predicted features is about 0.05 to 0.10, about four to fourteen times below raw accuracy, and below 0.05 for resting potential. For 13 Hodgkin-Huxley parameters fitted to the same cells in previous work, within-type and within-family R² are indistinguishable from zero, so family-level prediction reflects family means. Results hold with a second, curated channel gene list. Raw accuracy in this setting mostly measures how separable cell types are. Larger datasets should improve within-type prediction, but toward a ceiling several times below current raw figures.

Keywords: Patch-seq, ion channels, electrophysiology, cell types, cross-validation, effect size
