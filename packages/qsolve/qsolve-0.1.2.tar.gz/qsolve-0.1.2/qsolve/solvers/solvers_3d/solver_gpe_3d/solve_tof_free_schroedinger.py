from qsolve.core import qsolve_core


def solve_tof_free_schroedinger(self, kwargs):

    T_tof_free_schroedinger = kwargs["T_tof"] / self.units.unit_time

    self.psi_f_tof_free_schroedinger = qsolve_core.solve_tof_free_schroedinger_3d(
        self.psi_0_tof_free_schroedinger,
        self.x_0_tof_free_schroedinger,
        self.y_0_tof_free_schroedinger,
        self.z_0_tof_free_schroedinger,
        self.x_f_tof_free_schroedinger,
        self.y_f_tof_free_schroedinger,
        self.z_f_tof_free_schroedinger,
        T_tof_free_schroedinger,
        self.hbar,
        self.m_atom)
