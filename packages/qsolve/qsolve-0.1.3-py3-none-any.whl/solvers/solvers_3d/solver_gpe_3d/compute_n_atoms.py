from qsolve.core import qsolve_core


def compute_n_atoms(self, identifier):

    if identifier == "psi":

        n_atoms = qsolve_core.compute_n_atoms_gpe_3d(self.psi, self.dx, self.dy, self.dz)

    elif identifier == "psi_0":

        n_atoms = qsolve_core.compute_n_atoms_gpe_3d(self.psi_0, self.dx, self.dy, self.dz)

    else:

        message = 'identifier \'{0:s}\' not supported for this operation'.format(identifier)

        raise Exception(message)

        n_atoms = None

    return n_atoms
