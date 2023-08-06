from qsolve.potentials.potentials_3d import PotentialLesanovsky
from qsolve.potentials.potentials_3d import PotentialLesanovskyTiltX
from qsolve.potentials.potentials_3d import PotentialLesanovskyXYTiltX
from qsolve.potentials.potentials_3d import PotentialLesanovskyXYTiltXBoxZ
from qsolve.potentials.potentials_3d import PotentialHarmonicXYLatticeZ
from qsolve.potentials.potentials_3d import PotentialHarmonicXYGaussianZ
from qsolve.potentials.potentials_3d import PotentialHarmonic


def init_potential(self, params_user):

    params_solver = {
        "x": self.x,
        "y": self.y,
        "z": self.z,
        "Lx": self.Lx,
        "Ly": self.Ly,
        "Lz": self.Lz,
        "hbar": self.hbar,
        "mu_B": self.mu_B,
        "m_atom": self.m_atom,
        "unit_length": self.units.unit_length,
        "unit_time": self.units.unit_time,
        "unit_mass": self.units.unit_mass,
        "unit_energy": self.units.unit_energy,
        "unit_frequency": self.units.unit_frequency,
        "device": self.device
    }

    name = params_user['name']

    if name == "lesanovsky":

        self.potential = PotentialLesanovsky(params_solver, params_user)

    elif name == "lesanovsky_tilt_x":

        self.potential = PotentialLesanovskyTiltX(params_solver, params_user)

    elif name == "lesanovsky_xy_tilt_x":

        self.potential = PotentialLesanovskyXYTiltX(params_solver, params_user)

    elif name == "lesanovsky_xy_tilt_x_box_z":

        self.potential = PotentialLesanovskyXYTiltXBoxZ(params_solver, params_user)

    elif name == "harmonic_xy_lattice_z":

        self.potential = PotentialHarmonicXYLatticeZ(params_solver, params_user)

    elif name == "harmonic_xy_gaussian_z":

        self.potential = PotentialHarmonicXYGaussianZ(params_solver, params_user)

    elif name == "harmonic":

        self.potential = PotentialHarmonic(params_solver, params_user)

    else:

        message = 'init_potential(self, params): name \'{0:s}\' unknown'.format(name)

        raise Exception(message)
