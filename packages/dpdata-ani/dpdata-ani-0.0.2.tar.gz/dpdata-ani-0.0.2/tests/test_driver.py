import dpdata
import numpy as np


def test_ani_driver():
    s = dpdata.System(data={
        "atom_names": ["H"],
        "atom_numbs": [1],
        "atom_types": np.zeros((1,), dtype=int),
        "coords": np.zeros((1, 1, 3), dtype=np.float32),
        "cells": np.zeros((1, 3, 3), dtype=np.float32),
        "orig": np.zeros(3, dtype=np.float32),
        "nopbc": True,
    })
    ls = s.predict(driver="ani/1x")
    assert ls.get_natoms() == 1
    assert ls.get_nframes() == 1
