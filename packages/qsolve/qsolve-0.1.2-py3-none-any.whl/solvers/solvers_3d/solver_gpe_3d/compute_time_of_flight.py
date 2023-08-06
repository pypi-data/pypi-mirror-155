from qsolve.core import qsolve_core


def compute_time_of_flight(self, kwargs):

    print('----------------------------------------------------------------------------------------')
    print("time of flight:")

    self.psi_tof_free_gpe = qsolve_core.init_psi_tof_free_gpe(
        self.psi,
        self.Jx_tof_free_gpe,
        self.Jy_tof_free_gpe,
        self.Jz_tof_free_gpe)

    print("propagate psi_tof_free_gpe ...")

    self.psi_tof_free_gpe = qsolve_core.propagate_free_gpe_3d(
        self.psi_tof_free_gpe,
        self.dx_tof_free_gpe,
        self.dy_tof_free_gpe,
        self.dz_tof_free_gpe,
        self.dt_tof_free_gpe,
        self.n_time_steps_tof_free_gpe,
        self.hbar,
        self.m_atom,
        self.g)

    self.psi_0_tof_free_schroedinger = self.psi_tof_free_gpe

    print("compute psi_tof_free_schroedinger ...")

    self.psi_f_tof_free_schroedinger = qsolve_core.solve_tof_free_schroedinger_3d(
        self.psi_0_tof_free_schroedinger,
        self.x_0_tof_free_schroedinger,
        self.y_0_tof_free_schroedinger,
        self.z_0_tof_free_schroedinger,
        self.x_f_tof_free_schroedinger,
        self.y_f_tof_free_schroedinger,
        self.z_f_tof_free_schroedinger,
        self.T_tof_free_schroedinger,
        self.hbar,
        self.m_atom)

    print('----------------------------------------------------------------------------------------')

    print()
