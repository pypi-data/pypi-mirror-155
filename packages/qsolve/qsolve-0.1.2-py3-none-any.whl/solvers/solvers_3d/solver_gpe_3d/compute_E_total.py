from qsolve.core import qsolve_core


def compute_E_total(self, identifier, kwargs):

    if "units" in kwargs:

        units = kwargs["units"]

    else:

        units = "si_units"

    if identifier == "psi":

        E = qsolve_core.compute_E_total_gpe_3d(
            self.psi,
            self.V,
            self.dx,
            self.dy,
            self.dz,
            self.hbar,
            self.m_atom,
            self.g)

    elif identifier == "psi_0":

        E = qsolve_core.compute_E_total_gpe_3d(
            self.psi_0,
            self.V,
            self.dx,
            self.dy,
            self.dz,
            self.hbar,
            self.m_atom,
            self.g)

    else:

        message = 'compute_E_total(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)

    if units == "si_units":

        return self.units.unit_energy * E

    else:

        return E
