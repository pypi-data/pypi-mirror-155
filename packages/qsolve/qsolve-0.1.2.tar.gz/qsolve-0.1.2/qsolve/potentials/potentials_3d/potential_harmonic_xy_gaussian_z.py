from qsolve.core import qsolve_core


class PotentialHarmonicXYGaussianZ(object):

    def __init__(self, params_solver, params_user):

        x = params_solver["x"]
        y = params_solver["y"]
        z = params_solver["z"]

        m_atom = params_solver["m_atom"]

        unit_length = params_solver["unit_length"]
        unit_energy = params_solver["unit_energy"]
        unit_frequency = params_solver["unit_frequency"]

        omega_x = params_user["omega_x"] / unit_frequency
        omega_y = params_user["omega_y"] / unit_frequency

        V_harmonic_x = qsolve_core.eval_potential_harmonic_x_3d(x, y, z, omega_x, m_atom)
        V_harmonic_y = qsolve_core.eval_potential_harmonic_y_3d(x, y, z, omega_y, m_atom)

        self.V_harmonic_xy = V_harmonic_x + V_harmonic_y

        sigma_gaussian_z = params_user["sigma_gaussian"] / unit_length

        self.V_gaussian_z = qsolve_core.eval_potential_gaussian_z_3d(x, y, z, sigma_gaussian_z)

        self.V_ref_gaussian = params_user["V_ref_gaussian"] / unit_energy

    def eval(self, u):

        amplitude_gaussian_z = u * self.V_ref_gaussian

        return self.V_harmonic_xy + amplitude_gaussian_z * self.V_gaussian_z
