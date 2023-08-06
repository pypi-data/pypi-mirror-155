import dpdata
import numpy as np
from .auto_batch_size import AutoBatchSize
from dpdata.driver import Driver
from dpdata.periodic_table import Element


def ani_eval(model, device, coords: np.ndarray, species: np.ndarray):
    import torch
    from torchani.units import hartree2ev

    nframes = coords.shape[0]
    natoms = coords.shape[1]
    species = torch.tensor(species, device=device)
    coordinates = torch.tensor(coords,
                    requires_grad=True, device=device, dtype=torch.float32)
    energy = hartree2ev(model((species, coordinates)).energies)
    derivative = torch.autograd.grad(energy.sum(), coordinates)[0]
    force = -derivative
    energy = energy.cpu().detach().numpy().reshape((nframes,))
    force = force.cpu().detach().numpy().reshape((nframes, natoms, 3))
    return energy, force


@Driver.register("ani")
class ANIDriver(Driver):
    def __init__(self, model, device: str=None):
        import torch

        if device is None:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self.device = torch.device(device)
        self.model = model.to(self.device)
        self.auto_batch_size = AutoBatchSize()

    def label(self, data):
        nframes = data['coords'].shape[0]
        natoms = data['coords'].shape[1]

        atomic_z = np.array([Element(xx).Z for xx in data['atom_names']], dtype=int)

        species = np.array(atomic_z[data['atom_types']])
        species = np.tile(species, (nframes, 1))

        energy, force = self.auto_batch_size.execute_all(ani_eval, nframes, natoms, self.model, self.device, data['coords'], species)

        data['energies'] = energy
        data['forces'] = force
        return data


@Driver.register("ani/1x")
class ANI1xDriver(ANIDriver):
    def __init__(self, device: str=None, model_index: int=None):
        import torchani

        ANIDriver.__init__(self, torchani.models.ANI1x(periodic_table_index=True, model_index=model_index), device=device)


@Driver.register("ani/1ccx")
class ANI1ccxDriver(ANIDriver):
    def __init__(self, device: str=None, model_index: int=None):
        import torchani

        ANIDriver.__init__(self, torchani.models.ANI1ccx(periodic_table_index=True, model_index=model_index), device=device)


@Driver.register("ani/2x")
class ANI2xDriver(ANIDriver):
    def __init__(self, device: str=None, model_index: int=None):
        import torchani

        ANIDriver.__init__(self, torchani.models.ANI2x(periodic_table_index=True, model_index=model_index), device=device)
