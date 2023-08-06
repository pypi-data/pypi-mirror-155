from qsolve.core import qsolve_core


class PotentialHarmonic(object):

    def __init__(self, params_solver, params_user):

        x = params_solver["x"]
        y = params_solver["y"]
        z = params_solver["z"]

        m_atom = params_solver["m_atom"]

        unit_frequency = params_solver["unit_frequency"]

        omega_x = params_user["omega_x"] / unit_frequency
        omega_y = params_user["omega_y"] / unit_frequency
        omega_z = params_user["omega_z"] / unit_frequency

        self.V_harmonic = qsolve_core.eval_potential_harmonic_3d(x, y, z, omega_x, omega_y, omega_z, m_atom)

    def eval(self, u):

        return self.V_harmonic
