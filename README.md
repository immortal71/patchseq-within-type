# Ion channel expression and within-type electrophysiology (Patch-seq)

Code, results and figures for:

> Kharel A. *Ion channel expression mostly predicts neuronal cell identity, and only weakly predicts electrophysiology within a cell type.* 2026. Preprint: [DOI to be added]

The question: when ion channel gene expression predicts a neuron's electrophysiology, how much of that accuracy is a relationship *within* a transcriptomic cell type, and how much is just telling cell types apart?

Main results (mouse motor cortex, Scala et al. 2021):

- Mean cross-validated R² across 29 features: 0.270 raw, 0.0024 after removing type means (same cells).
- 12 of 29 features keep a within-type residual above a permutation null (7 after FDR); resting potential keeps none (p = 0.76).
- Calibrating against planted effects, the true within-type R² for the best-predicted features is about 0.05 to 0.10, roughly 4 to 14 times below raw.
- Fitted Hodgkin-Huxley parameters (Bernaerts et al. 2025): within-type and within-family R² are about zero.

## Reproduce

```sh
pip install -r requirements.txt
./get_data.sh                      # clones the two public Berens lab repos into data/
python scripts/01_baseline.py      # raw vs within-type, 29 features
python scripts/02_permutation.py   # 500x within-type permutation null + family control
python scripts/09_foldwise.py      # type means estimated inside training folds
python scripts/10_calibration.py   # planted-effect calibration (needs 02 output)
python scripts/04_power.py         # earlier power check, dense and sparse signals
python scripts/05_labels_genesets.py  # non-channel clusters, HGNC gene list
python scripts/06_hcn.py           # Hcn1-4 test
python scripts/08_hh.py            # fitted Hodgkin-Huxley parameters
python scripts/07_figures.py       # figures from results/*.csv
```

Run from the repository root. Total runtime is a few hours on two CPU cores; 02 and 10 are the longest.

### Visual cortex replication

`scripts/v1_replication.py` applies the same pipeline to the Allen mouse visual cortex Patch-seq release (Gouwens et al. 2020). It needs `V1_features.pickle` (from `data/hh_sbi/code/pickles/`) and two Allen files: `20200625_patchseq_metadata_mouse.csv` and `20200513_Mouse_PatchSeq_Release_count.csv`. These were not reachable from the environment the paper was produced in, so this result is not in the paper.

```sh
python scripts/v1_replication.py --features data/hh_sbi/code/pickles/V1_features.pickle \
  --meta 20200625_patchseq_metadata_mouse.csv --counts 20200513_Mouse_PatchSeq_Release_count.csv
```

## Layout

- `scripts/` analysis code (`core.py` holds the shared pipeline)
- `results/` every number in the paper, as CSV
- `figures/` PNG and PDF figures
- `manuscript/` the article (Markdown sources, `build.py`, Word, PDF)

## License

MIT for code. Input data belong to their original authors and keep their licenses.
