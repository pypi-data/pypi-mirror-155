from qsolve.core import qsolve_core


class PotentialLesanovsky(object):

    def __init__(self, params_solver, params_user):

        self.x = params_solver["x"]
        self.y = params_solver["y"]
        self.z = params_solver["z"]

        self.hbar = params_solver["hbar"]
        self.mu_B = params_solver["mu_B"]
        self.m_atom = params_solver["m_atom"]

        unit_frequency = params_solver["unit_frequency"]

        self.g_F = params_user["g_F"]
        self.m_F = params_user["m_F"]
        self.m_F_prime = params_user["m_F_prime"]

        self.omega_perp = params_user["omega_perp"] / unit_frequency
        self.omega_para = params_user["omega_para"] / unit_frequency
        self.omega_delta_detuning = params_user["omega_delta_detuning"] / unit_frequency
        self.omega_trap_bottom = params_user["omega_trap_bottom"] / unit_frequency
        self.omega_rabi_ref = params_user["omega_rabi_ref"] / unit_frequency

    def eval(self, u):

        omega_rabi = u * self.omega_rabi_ref

        return qsolve_core.eval_potential_lesanovsky_3d(
            self.x,
            self.y,
            self.z,
            self.g_F,
            self.m_F,
            self.m_F_prime,
            self.omega_perp,
            self.omega_para,
            self.omega_delta_detuning,
            self.omega_trap_bottom,
            omega_rabi,
            self.hbar,
            self.mu_B,
            self.m_atom)
