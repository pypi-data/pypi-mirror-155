# dpdata_ani

The [dpdata](https://github.com/deepmodeling/dpdata) plugin for ANI.

## Features

- `ani/1x` format to load [ANI-1x dataset](https://doi.org/10.1038/s41597-020-0473-z)
- `ani/1x`, `ani/2x`, and `ani/1ccx` driver to predict using ANI models with automatic batch size

## Installation

```sh
pip install git+https://github.com/njzjz/dpdata_ani
```

## Usage

First, download ANI-1x dataset:
```sh
wget https://figshare.com/ndownloader/files/18112775 -O ani1x.hdf5
```

Load the ANI-1x dataset, and predict it with ANI-2x models:
```py
import dpdata
ani = dpdata.MultiSystems().from_ani_1x("ani1x.hdf5")
predict = ani.predict(driver="ani/2x")
predict.to_deepmd_hdf5("predict.hdf5")
```

The inferred data will be stored in `predict.hdf5`.
