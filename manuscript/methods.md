## Methods

### Data

Mouse primary motor cortex Patch-seq data (Scala et al. 2021) were taken from the public mini-atlas repository (github.com/berenslab/mini-atlas): exon and intron count matrices, 29 electrophysiological features, cell metadata including transcriptomic family and type, and gene lengths. Fitted Hodgkin-Huxley parameters (maximum a posteriori sample per cell, 13 parameters) were taken from the hh_sbi repository (github.com/berenslab/hh_sbi) released with Bernaerts et al. (2025). No new animal or human data were generated, so no ethics approval was required.

### Expression preprocessing

Exon and intron counts were summed per gene, converted to reads per kilobase per million (library size over all genes, length from the released gene_bp column) and transformed with log(1 + x). Channel genes were selected by prefix over standard channel families (potassium, sodium, calcium and chloride channels; HCN; TRP; connexins and pannexins; anoctamins and bestrophins; acid-sensing; P2X; ionotropic GABA, glycine, glutamate, nicotinic and 5-HT3 receptors; ryanodine and IP3 receptors; Piezo; LRRC8; tweety; NALCN; Orai; CatSper; TPC; Hv1; CLIC; ZAC; polycystin-2; mucolipin; CNG; CFTR; TMC; otopetrin; CALHM). Genes detected in fewer than 10 cells were removed, a filter that does not use labels or targets. This left 390 genes. As a robustness check, the HGNC ion channel gene group shipped with the mini-atlas repository was used instead (human symbols mapped to mouse by case).

### Regression

Each feature was predicted with ridge regression under 10-fold cross-validation. Inside each training fold, predictors were standardized with training-fold statistics and the penalty was chosen by generalized cross-validation over 30 log-spaced values from 0.01 to 100,000. Test-fold standardized values were clipped to the range seen in the training fold; without this, a gene that is almost constant in one training fold produced extreme predictions for single test cells. R² was computed once on the pooled held-out predictions against the total sum of squares. For comparison, the same outer folds were used with two other estimators. Elastic net was fitted per feature, with penalty strength (30 values) and l1 ratio (0.1, 0.5 or 0.9) chosen by inner 5-fold cross-validation in each training fold. Reduced-rank ridge regression fitted all 29 standardized features jointly: a ridge fit with the penalty chosen by generalized cross-validation, whose coefficients were then projected onto the top two or five right singular vectors of the fitted training values.

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

Within type, Hcn1 to Hcn4 were used as the only predictors for seven features and compared with 500 random sets of four other channel genes. Leave-one-gene-out and Hcn1-only fits were also run. The four-gene test and its seven features were fixed before the test was first run.

### Visual cortex replication

A script that applies the same pipeline to the mouse visual cortex Patch-seq release of Gouwens et al. (2020), using the 23 features extracted by Bernaerts et al. (2025), is provided. That release contains exon counts without gene lengths, so expression is log(1 + counts per million).

### Software and availability

Python 3 with NumPy, pandas and scikit-learn 1.9. All scripts download or read only public inputs and are available at https://github.com/immortal71/patchseq-within-type and archived on Zenodo (https://doi.org/10.5281/zenodo.23451340).

### Use of AI tools

An AI assistant (Claude, Anthropic) was used to write and debug analysis code, run analyses, check references against PubMed, draft and edit text, and make figures. The author directed the research question and analysis plan, reviewed every result and all text, and takes full responsibility for the content.
