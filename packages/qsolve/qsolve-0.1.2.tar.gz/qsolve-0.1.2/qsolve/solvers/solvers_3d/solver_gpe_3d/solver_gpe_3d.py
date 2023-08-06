from qsolve.solvers.solvers_3d.solver_gpe_3d.init_seed import init_seed
from qsolve.solvers.solvers_3d.solver_gpe_3d.init_device import init_device
from qsolve.solvers.solvers_3d.solver_gpe_3d.init_units import init_units

from qsolve.solvers.solvers_3d.solver_gpe_3d.init_grid import init_grid

from qsolve.solvers.solvers_3d.solver_gpe_3d.init_sgpe_z_eff import init_sgpe_z_eff

from qsolve.solvers.solvers_3d.solver_gpe_3d.init_potential import init_potential

from qsolve.solvers.solvers_3d.solver_gpe_3d.init_time_of_flight import init_time_of_flight
from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_time_of_flight import compute_time_of_flight

from qsolve.solvers.solvers_3d.solver_gpe_3d.init_grid_tof_free_gpe import init_grid_tof_free_gpe
from qsolve.solvers.solvers_3d.solver_gpe_3d.init_psi_tof_free_gpe import init_psi_tof_free_gpe
from qsolve.solvers.solvers_3d.solver_gpe_3d.propagate_tof_free_gpe import propagate_tof_free_gpe

from qsolve.solvers.solvers_3d.solver_gpe_3d.init_grid_tof_free_schroedinger import init_grid_tof_free_schroedinger
from qsolve.solvers.solvers_3d.solver_gpe_3d.set_psi_0_tof_free_schroedinger import set_psi_0_tof_free_schroedinger
from qsolve.solvers.solvers_3d.solver_gpe_3d.solve_tof_free_schroedinger import solve_tof_free_schroedinger

from qsolve.solvers.solvers_3d.solver_gpe_3d.init_time_evolution import init_time_evolution

from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_ground_state_solution import compute_ground_state_solution
from qsolve.solvers.solvers_3d.solver_gpe_3d.propagate_gpe import propagate_gpe
from qsolve.solvers.solvers_3d.solver_gpe_3d.propagate_sgpe_z_eff import propagate_sgpe_z_eff

from qsolve.solvers.solvers_3d.solver_gpe_3d.set_psi import set_psi
from qsolve.solvers.solvers_3d.solver_gpe_3d.set_V import set_V
from qsolve.solvers.solvers_3d.solver_gpe_3d.set_u_of_times import set_u_of_times

from qsolve.solvers.solvers_3d.solver_gpe_3d.getter_functions import get

from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_n_atoms import compute_n_atoms

from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_chemical_potential import compute_chemical_potential

from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_E_total import compute_E_total
from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_E_kinetic import compute_E_kinetic
from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_E_potential import compute_E_potential
from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_E_interaction import compute_E_interaction

from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_density_xy import compute_density_xy
from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_density_xz import compute_density_xz

from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_spectrum_abs_xy import compute_spectrum_abs_xy
from qsolve.solvers.solvers_3d.solver_gpe_3d.compute_spectrum_abs_xz import compute_spectrum_abs_xz


class SolverGPE3D(object):

    def __init__(self, **kwargs):

        init_seed(self, kwargs)
        init_device(self, kwargs)
        init_units(self, kwargs)

    def init_grid(self, **kwargs):
        init_grid(self, kwargs)

    def init_potential(self, params):
        init_potential(self, params)

    def init_time_of_flight(self, params):
        init_time_of_flight(self, params)

    def compute_time_of_flight(self, **kwargs):
        compute_time_of_flight(self, kwargs)

    def init_sgpe_z_eff(self, **kwargs):
        init_sgpe_z_eff(self, kwargs)

    def set_V(self, **kwargs):
        set_V(self, kwargs)

    def set_psi(self, identifier, **kwargs):
        set_psi(self, identifier, kwargs)

    def set_u_of_times(self, u_of_times):
        set_u_of_times(self, u_of_times)

    def compute_ground_state_solution(self, **kwargs):
        compute_ground_state_solution(self, kwargs)

    def propagate_sgpe_z_eff(self, **kwargs):
        propagate_sgpe_z_eff(self, kwargs)

    def init_time_evolution(self, **kwargs):
        init_time_evolution(self, kwargs)

    def propagate_gpe(self, **kwargs):
        propagate_gpe(self, kwargs)

    def init_grid_tof_free_gpe(self, **kwargs):
        init_grid_tof_free_gpe(self, kwargs)

    def init_psi_tof_free_gpe(self, identifier, **kwargs):
        init_psi_tof_free_gpe(self, identifier, kwargs)

    def propagate_tof_free_gpe(self, **kwargs):
        propagate_tof_free_gpe(self, kwargs)

    def init_grid_tof_free_schroedinger(self, **kwargs):
        init_grid_tof_free_schroedinger(self, kwargs)

    def set_psi_0_tof_free_schroedinger(self, identifier, **kwargs):
        set_psi_0_tof_free_schroedinger(self, identifier, kwargs)

    def solve_tof_free_schroedinger(self, **kwargs):
        solve_tof_free_schroedinger(self, kwargs)

    def get(self, identifier, **kwargs):
        return get(self, identifier, kwargs)

    def compute_n_atoms(self, identifier):
        return compute_n_atoms(self, identifier)

    def compute_chemical_potential(self, identifier, **kwargs):
        return compute_chemical_potential(self, identifier, kwargs)

    def compute_E_total(self, identifier, **kwargs):
        return compute_E_total(self, identifier, kwargs)

    def compute_E_kinetic(self, identifier, **kwargs):
        return compute_E_kinetic(self, identifier, kwargs)

    def compute_E_potential(self, identifier, **kwargs):
        return compute_E_potential(self, identifier, kwargs)

    def compute_E_interaction(self, identifier, **kwargs):
        return compute_E_interaction(self, identifier, kwargs)

    def compute_density_xy(self, identifier, **kwargs):
        return compute_density_xy(self, identifier, kwargs)

    def compute_density_xz(self, identifier, **kwargs):
        return compute_density_xz(self, identifier, kwargs)

    def compute_spectrum_abs_xy(self, identifier, **kwargs):
        return compute_spectrum_abs_xy(self, identifier, kwargs)

    def compute_spectrum_abs_xz(self, identifier, **kwargs):
        return compute_spectrum_abs_xz(self, identifier, kwargs)
