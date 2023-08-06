# Introduction to TensorFlow

The purpose of this repository is to provide a walk through common examples and workflows when working with TensorFlow 2.0

## Set up

### Mac M2

First, make sure the ARM64 installation of Anaconda is installed on your machine.

Then, create an anaconda virtual environment that only consists of the following:

```bash
conda create -n apple-tensorflow-deps python=3.10.11
conda activate apple-tensorflow-deps
conda install -c apple tensorflow-deps
```

Then, make sure to install `poetry` using `brew`:

```bash
brew install poetry
```

Then you can clone this repo, and install the dependencies with poetry:

```bash
# use the Python found inside your conda apple-tensorflow-deps environment
poetry env use $(which python)
# install all dependencies
poetry install
```
