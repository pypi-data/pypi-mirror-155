# pydiverse.pipetest

[![CI](https://github.com/pydiverse/pydiverse.pipetest/actions/workflows/ci.yml/badge.svg)](https://github.com/pydiverse/pydiverse.pipetest/actions/workflows/ci.yml)

An adaption layer for pydiverse.pipedag that simplyfies execution of pipedag steps as unit tests with cache invalidation awareness.

## Installation

You can install the package in development mode using:

```bash
git clone https://github.com/pydiverse/pydiverse.pipetest.git
cd pydiverse.pipetest

# create and activate a fresh environment named pydiverse.pipetest
# see environment.yml for details
mamba env create
conda activate pydiverse.pipetest

pre-commit install
pip install --no-build-isolation -e .
```
