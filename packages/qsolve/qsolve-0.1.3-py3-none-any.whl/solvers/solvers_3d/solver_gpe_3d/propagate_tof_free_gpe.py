from qsolve.core import qsolve_core


def propagate_tof_free_gpe(self, kwargs):

    self.psi_tof_free_gpe = qsolve_core.propagate_free_gpe_3d(
        self.psi_tof_free_gpe,
        self.dx_tof_free_gpe,
        self.dy_tof_free_gpe,
        self.dz_tof_free_gpe,
        self.dt_tof_free_gpe,
        kwargs["n_inc"],
        self.hbar,
        self.m_atom,
        self.g)
