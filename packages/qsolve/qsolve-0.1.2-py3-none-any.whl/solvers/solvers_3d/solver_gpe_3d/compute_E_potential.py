from qsolve.core import qsolve_core


def compute_E_potential(self, identifier, kwargs):

    if "units" in kwargs:

        units = kwargs["units"]

    else:

        units = "si_units"

    if identifier == "psi":

        E_potential = qsolve_core.compute_E_potential_gpe_3d(
            self.psi,
            self.V,
            self.dx,
            self.dy,
            self.dz)

    elif identifier == "psi_0":

        E_potential = qsolve_core.compute_E_potential_gpe_3d(
            self.psi_0,
            self.V,
            self.dx,
            self.dy,
            self.dz)

    else:

        message = 'compute_E_potential(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)

    if units == "si_units":

        return self.units.unit_energy * E_potential

    else:

        return E_potential
