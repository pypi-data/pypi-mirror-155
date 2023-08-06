import h5py
import numpy as np
import dpdata
from dpdata.format import Format

unitconv = dpdata.unit.EnergyConversion("hartree", "eV").value()

@Format.register("ani/1x")
@Format.register("ani/1ccx")
class ANI1xFormat(Format):
    """ANI-1x dataset loader. The dataset can be downloaded from
    https://doi.org/10.1038/s41597-020-0473-z
    """
    def from_labeled_system(self, sub, **kwargs):
        atom_symbols = np.array(dpdata.periodic_table.ELEMENTS)[sub['atomic_numbers'][:] - 1]
        atom_names, atom_types, atom_numbs = np.unique(atom_symbols, return_inverse=True, return_counts=True)
        nframes = sub['coordinates'][:].shape[0]
        return { 
            "atom_names":list(atom_names),
            "atom_types":atom_types,
            "atom_numbs":list(atom_numbs),
            "coords":sub['coordinates'][:],
            "energies":sub['wb97x_dz.energy'][:] * unitconv,
            "forces":sub['wb97x_dz.forces'][:] * unitconv,                                                                                                                                                                                                                                                                    
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
                yield f[key]
