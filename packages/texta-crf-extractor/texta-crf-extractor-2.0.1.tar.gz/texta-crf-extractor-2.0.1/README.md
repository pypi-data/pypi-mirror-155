# TEXTA CRF Extractor

## Requirements

* Python >= 3.8
* SciPy installation for scikit-learn (requires BLAS & LAPACK system libraries).

## Installation:

```
# For debian based systems (ex: debian:buster) to install binary dependencies.

apt-get update && apt-get install python3-scipy

# Install without MLP

pip install texta-crf-extractor

# Install with MLP 

pip install texta-crf-extractor[mlp]

```

## Usage:

```
from texta_crf_extractor.crf_extractor import CRFExtractor
from texta_mlp.mlp import MLP

mlp = MLP(language_codes=["en"], default_language_code="en")

# prepare data
texts = ["foo", "bar"]
mlp_docs = [mlp.process(text) for text in texts]

# create extractor
extractor = CRFExtractor(mlp=mlp)

# train the CRF model
extractor.train(mlp_docs)

# tag something
extractor.tag("Tere maailm!")

```
