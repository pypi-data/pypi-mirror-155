from qsolve.core import qsolve_core


def propagate_sgpe_z_eff(self, kwargs):

    self.psi = qsolve_core.propagate_sgpe_z_eff_3d(
        self.psi,
        self.V,
        self.dx,
        self.dy,
        self.dz,
        self.dt_sgpe,
        kwargs["n_inc"],
        self.T_des_sgpe,
        self.mue_des_sgpe,
        self.gamma_sgpe,
        self.hbar,
        self.k_B,
        self.m_atom,
        self.g)

    self.psi = self.filter_z_sgpe * self.psi
