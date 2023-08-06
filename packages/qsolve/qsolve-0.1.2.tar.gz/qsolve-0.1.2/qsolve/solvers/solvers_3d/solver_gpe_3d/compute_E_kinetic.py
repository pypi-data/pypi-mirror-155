from qsolve.core import qsolve_core


def compute_E_kinetic(self, identifier, kwargs):

    if "units" in kwargs:

        units = kwargs["units"]

    else:

        units = "si_units"

    if identifier == "psi":

        E_kinetic = qsolve_core.compute_E_kinetic_gpe_3d(
            self.psi,
            self.dx,
            self.dy,
            self.dz,
            self.hbar,
            self.m_atom)

    elif identifier == "psi_0":

        E_kinetic = qsolve_core.compute_E_kinetic_gpe_3d(
            self.psi_0,
            self.dx,
            self.dy,
            self.dz,
            self.hbar,
            self.m_atom)

    elif identifier == "psi_tof_free_gpe":

        E_kinetic = qsolve_core.compute_E_kinetic_gpe_3d(
            self.psi_tof_free_gpe,
            self.dx_tof_free_gpe,
            self.dy_tof_free_gpe,
            self.dz_tof_free_gpe,
            self.hbar,
            self.m_atom)

    else:

        message = 'compute_E_kinetic(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)

    if units == "si_units":

        return self.units.unit_energy * E_kinetic

    else:

        return E_kinetic
