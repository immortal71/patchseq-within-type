#!/bin/sh
# Downloads the public inputs (about 600 MB) into data/.
set -e
mkdir -p data
git clone --depth 1 https://github.com/berenslab/mini-atlas data/mini-atlas
git clone --depth 1 https://github.com/berenslab/hh_sbi data/hh_sbi
