## Discussion

Across all cells, ion channel expression predicts many electrophysiological features well. Within a transcriptomic type, it predicts very little, and what it does predict is far smaller than the raw figures suggest. After correcting cross-validated R² for the attenuation that affects weak effects at this sample size, the within-type relationship for the best-predicted features is around R² 0.05 to 0.10, four to fourteen times below the raw accuracy on the same cells. For resting membrane potential, there is no detectable within-type relationship at all.

### What raw accuracy measures

The simplest reading is that a regression from channel expression to physiology combines two real relationships: channel expression identifies cell type, and cell type largely determines physiology. Voltage-gated channel genes are good type markers, so a model can score highly across cells while learning mostly which type a cell belongs to. Raw accuracy still ranks features in roughly the right order of within-type signal (ρ = 0.75). It should not be read as the strength of a gene-to-function link inside a cell type, and claims of that kind need a within-type figure alongside the raw one.

This fits older evidence that cells of one type reach similar behaviour with different channel complements (Schulz et al. 2006; Marder & Goaillard 2006; Goaillard & Marder 2021), the finding that many cross-type gene to property correlations are class-driven (Bomkamp et al. 2019), and the observation from this same dataset that types within a family are poorly separated electrophysiologically (Scala et al. 2021). Biophysical models of cortical neurons point the same way: electrical features depend on synergistic combinations of conductances, whereas channel gene expression in single cells is dominated by redundancy (Reva et al. 2025). Transcript abundance also captures only one factor of membrane conductance. Conductance depends on channel number, open probability and single-channel conductance, and the mRNA count is a noisy proxy for the first of these only. Trafficking, subunit composition and modulation are invisible to it.

### Data size, revisited

Bernaerts et al. (2025) attributed the loss of accuracy at the level of fine types to limited data. The near-zero values invite the opposite reading, that the within-type quantity is too small for more data to matter. The power analysis shows that reading goes too far. At roughly 950 cells and 390 genes, a within-type effect of R² 0.05 is detected only about half the time, so the near-zero observed values are consistent with real effects of that size, and more cells would recover more of them.

What the analysis does support is a ceiling. For most features with a surviving residual, the implied true within-type R² is at or below about 0.15 even at the upper end of its range, and for resting membrane potential it is below about 0.05. Larger datasets should improve within-type prediction, and the value they approach is several times smaller than current raw figures. The two accounts, insufficient data and a small target, are both partly right, and the useful quantity for planning future datasets is the size of that target.

For fitted Hodgkin-Huxley parameters, within-type and within-family R² are indistinguishable from zero, and family-level prediction is carried by family means. The mechanistic interpretability of a model parameter does not by itself establish that its gene-to-parameter mapping holds within a cell type.

### The resting potential null and the Ih exception

Resting potential is set by small leak currents near equilibrium, pump activity and intracellular ion concentrations, none of which channel transcript counts capture. This matters for attempts to infer resting potential from channel expression, including in tissues outside the nervous system. Within a cell type, this dataset gives no support for that inference.

The sag-related residual traces mainly to Hcn1. HCN channels have small single-channel conductance but are numerous and partly open near rest, so Ih may scale with channel number more directly than most currents. The model of Bernaerts et al. contains no hyperpolarization-activated current and was fitted to depolarizing steps, so it could not represent this effect even if present. The Hcn1 result was found after a four-gene test and is small; it needs replication in an independent dataset with hyperpolarizing protocols.

### Scope

The same decomposition applies to any method that infers a functional quantity from expression of the genes that implement it, such as metabolic flux, transcription factor activity or ligand-receptor communication, wherever cell types differ in both expression and function. Reporting a within-type control, with an estimate of how much a weak within-type effect would be attenuated at the available sample size, would make such claims easier to interpret.

### Limitations

All results come from one dataset, one brain region and one species. A script to repeat the main analysis on the larger mouse visual cortex Patch-seq release is provided but could not be run here because its count matrix was not reachable from the analysis environment. Transcriptomic types are defined from the transcriptome, partly including channel genes. Clusters built without any channel gene agreed only modestly with the published types and left more residual, so this check cannot exclude some circularity. The calibration assumes a linear, dense or sparse signal over the same genes; a nonlinear relationship could be recovered differently. Fitted model parameters are point estimates from a degenerate posterior, which attenuates raw and residual estimates alike. A learning curve was attempted and is not reported. Subsampling cells shrinks every type, and with fewer than about 10 cells per type both ways of removing type means are biased, in opposite directions, so the curve could not separate effect size from estimation error.
