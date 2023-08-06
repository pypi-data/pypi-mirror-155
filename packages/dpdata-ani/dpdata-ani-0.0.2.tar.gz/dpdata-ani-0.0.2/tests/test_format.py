import dpdata
import pytest
from pathlib import Path


def test_load_ani1x(tmp_path):
    fn = Path(__file__).parent / "anismall.hdf5"
    ms = dpdata.MultiSystems().from_ani_1x(fn)
    assert len(ms)
