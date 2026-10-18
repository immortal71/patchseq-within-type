## Figure legends

**Figure 1. Channel expression predicts electrophysiology across cell types but barely within them.** (a) Cross-validated ridge R² for 29 features from 390 channel genes, on the 946 to 969 cells in the 28 transcriptomic types with at least 15 cells. Blue: raw. Orange: after removing type means from expression and target. (b) Raw against within-type R² per feature. Circled points beat their within-type permutation null (500 permutations, p < 0.05). Note the different axis scales.

**Figure 2. Calibrating within-type R² against planted effects.** (a) Linear signals of known size were added to within-type-permuted residual targets and scored with the same pipeline (30 repeats per level, averaged over ten features; band shows the mean 10th to 90th percentile). Weak effects are recovered at a small fraction of their true size. (b) For each calibrated feature: raw R² on the same cells (blue), observed within-type R² (black tick) and the implied true within-type R² with its range (orange).

**Figure 3. Fitted Hodgkin-Huxley parameters.** Cross-validated R² for the 13 maximum a posteriori parameters of Bernaerts et al. (2025), predicted from their 427-gene set. Raw on the 668 cells of the 19 types with at least 15 cells (blue), after removing family means (grey; 942 cells, 7 families) and after removing type means (orange).

**Figure 4. How much residual survives depends on how finely identity is removed.** Distribution across the 29 features of within-group R² after removing means of transcriptomic families, of k-means clusters built from non-channel genes only (k = 30 and 50), of published transcriptomic types, and of published types with the HGNC channel gene list.

**Figure 5. HCN genes and sag within type.** Within-type R² using Hcn1 to Hcn4 as the only predictors (orange bars), Hcn1 alone (blue dots), and the 95th percentile of 500 random four-gene channel sets (black ticks), with permutation p values.

## Data and code availability

All input data are public: github.com/berenslab/mini-atlas (Scala et al. 2021) and github.com/berenslab/hh_sbi (Bernaerts et al. 2025). Every analysis script, result table and figure script is available at https://github.com/immortal71/patchseq-within-type under the MIT licence and archived on Zenodo (https://doi.org/10.5281/zenodo.23451340). The visual cortex replication script requires the Allen Institute mouse visual cortex Patch-seq release (Gouwens et al. 2020).

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

Reva M, Arnaudon A, Zbili M, Makkeh A, Markram H, Goaillard JM, Van Geit W. Higher-order interactions in neuronal function: from genes to ionic currents in biophysical models. Proc Natl Acad Sci U S A. 2025;122(40):e2500048122. doi:10.1073/pnas.2500048122

Scala F, Kobak D, Bernabucci M, et al. Phenotypic variation of transcriptomic cell types in mouse motor cortex. Nature. 2021;598(7879):144-150. doi:10.1038/s41586-020-2907-3

Schulz DJ, Goaillard JM, Marder E. Variable channel expression in identified single and electrically coupled neurons in different animals. Nat Neurosci. 2006;9(3):356-362. doi:10.1038/nn1639

Tripathy SJ, Toker L, Li B, et al. Transcriptomic correlates of neuron electrophysiological diversity. PLoS Comput Biol. 2017;13(10):e1005814. doi:10.1371/journal.pcbi.1005814
