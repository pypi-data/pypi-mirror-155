import h5py
import numpy as np
import dpdata
from dpdata.format import Format

unitconv = dpdata.unit.EnergyConversion("hartree", "eV").value()

@Format.register("ani/comp6")
class COMP6Format(Format):
    """COMP6 dataset loader. The dataset can be downloaded from
    https://github.com/isayev/COMP6
    """
    def from_labeled_system(self, sub, **kwargs):
        atom_symbols = list(map(lambda x:x.decode("utf-8") , sub['species'][:]))
        atom_names, atom_types, atom_numbs = np.unique(atom_symbols, return_inverse=True, return_counts=True)
        nframes = sub['coordinates'][:].shape[0]
        return {
            "atom_names": list(atom_names),
            "atom_types": atom_types,
            "atom_numbs": list(atom_numbs),
            "coords": sub['coordinates'][:],
            "energies": sub['energies'][:] * unitconv,
            "forces": -sub['forces'][:] * unitconv,
            "orig": np.array([0,0,0]),
            "cells": np.zeros((nframes, 3, 3)),
            "nopbc": True,
        }

    def from_multi_systems(self, hdf_file: str, **kwargs):
        """load from HDF5 file

        Parameters
        ----------
        hdf_file : str
            ANI-1x HDF5 file
        """
        with h5py.File(hdf_file, 'r') as f:
            for key in f.keys():
                if 'species' in f[key].keys():
                    yield f[key]
                else:
                    for key2 in f[key].keys():
                        yield f[key][key2]

