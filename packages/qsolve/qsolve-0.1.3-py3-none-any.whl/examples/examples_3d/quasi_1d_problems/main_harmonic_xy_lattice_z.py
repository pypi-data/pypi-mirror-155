from qsolve.solvers.solvers_3d.solver_gpe_3d import SolverGPE3D

import mkl
import os

import h5py

import numpy as np

from scipy import constants

from scipy import interpolate

import matplotlib.pyplot as plt

from figures.figure_main.figure_main import FigureMain

from evaluation import eval_data

# -------------------------------------------------------------------------------------------------
num_threads_cpu = 8

os.environ["OMP_NUM_THREADS"] = str(num_threads_cpu)
os.environ["MKL_NUM_THREADS"] = str(num_threads_cpu)

mkl.set_num_threads(num_threads_cpu)

assert(mkl.get_max_threads() == num_threads_cpu)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
pi = constants.pi

hbar = constants.hbar

amu = constants.physical_constants["atomic mass constant"][0]  # atomic mass unit

mu_B = constants.physical_constants["Bohr magneton"][0]

k_B = constants.Boltzmann
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# close figures from previous simulation

plt.close('all')
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
export_frames_figure_main = False

export_hdf5 = False

export_psi_of_times_analysis = False
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
N = 2000

m_Rb_87 = 87 * amu

m_atom = m_Rb_87

a_s = 5.24e-9

omega_perp = 2 * np.pi * 1e3

Jx = 48
Jy = 48
Jz = 256

t_final = 8e-3
dt = 0.0025e-3

x_min = -1.5e-6
x_max = +1.5e-6

y_min = -1.5e-6
y_max = +1.5e-6

z_min = -20e-6
z_max = +20e-6

params_potential = {
    "name": 'harmonic_xy_lattice_z',
    "omega_x": omega_perp,
    "omega_y": omega_perp,
    "V_lattice_z_max": 2.0 * omega_perp * hbar,
    "V_lattice_z_m": 8
}
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
simulation_id = params_potential['name']

simulation_id = simulation_id.replace(".", "_")
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# hdf5

path_f_hdf5 = "./data_hdf5/"

filepath_f_hdf5 = path_f_hdf5 + simulation_id + ".hdf5"
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# frames

path_frames_figure_main = "./frames/frames_figure_main/" + simulation_id + "/"

nr_frame_figure_main = 0

if export_frames_figure_main:

    if not os.path.exists(path_frames_figure_main):

        os.makedirs(path_frames_figure_main)
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# init solver and its potential
# =================================================================================================

solver = SolverGPE3D(m_atom=m_Rb_87,
                     a_s=a_s,
                     seed=1,
                     device='cuda:0',
                     num_threads_cpu=num_threads_cpu)

solver.init_grid(x_min=x_min,
                 x_max=x_max,
                 y_min=y_min,
                 y_max=y_max,
                 z_min=z_min,
                 z_max=z_max,
                 Jx=Jx,
                 Jy=Jy,
                 Jz=Jz)

solver.init_potential(params_potential)

x = solver.get('x')
y = solver.get('y')
z = solver.get('z')


# =================================================================================================
# init time evolution
# =================================================================================================

solver.init_time_evolution(t_final=t_final, dt=dt)

times = solver.get('times')

n_times = times.size
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
n_mod_times_analysis = 50

times_analysis = times[0::n_mod_times_analysis]

n_times_analysis = times_analysis.size

assert (times_analysis[-1] == t_final)
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# init control inputs
# =================================================================================================

# -------------------------------------------------------------------------------------------------
t0 = 0e-3
t1 = 1e-3
t2 = 2e-3
t3 = 3e-3

u0 = 1.0
u1 = 1.0
u2 = 0.0
u3 = 0.0

vec_t = np.array([t0, t1, t2, t3])
vec_u = np.array([u0, u1, u2, u3])

f = interpolate.PchipInterpolator(vec_t, vec_u)

u_of_times = f(times)
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# compute ground state solution psi_0
# =================================================================================================

# -------------------------------------------------------------------------------------------------
u_0 = u_of_times[0]

solver.set_V(u=u_0)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
solver.compute_ground_state_solution(N=N, n_iter=5000, tau=0.005e-3)

psi_0 = solver.get('psi_0')

N_psi_0 = solver.compute_n_atoms('psi_0')
mue_psi_0 = solver.compute_chemical_potential('psi_0')
E_psi_0 = solver.compute_E_total('psi_0')

print('N_psi_0 = {:1.16e}'.format(N_psi_0))
print('mue_psi_0 / h: {0:1.6} kHz'.format(mue_psi_0 / (1e3 * (2 * pi * hbar))))
print('E_psi_0 / (N_psi_0*h): {0:1.6} kHz'.format(E_psi_0 / (1e3 * (2 * pi * hbar * N_psi_0))))
print()
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# set wave function psi to ground state solution psi_0
# =================================================================================================

solver.set_psi('numpy', array=psi_0)

N_psi = solver.compute_n_atoms('psi')
mue_psi = solver.compute_chemical_potential('psi')
E_psi = solver.compute_E_total('psi')

print('N_psi = {:1.16e}'.format(N_psi))
print('mue_psi / h: {0:1.6} kHz'.format(mue_psi / (1e3 * (2 * pi * hbar))))
print('E_psi / (N_psi*h): {0:1.6} kHz'.format(E_psi / (1e3 * (2 * pi * hbar * N_psi))))
print()


# =================================================================================================
# init figure
# =================================================================================================

density_0 = np.abs(psi_0)**2
density_0_max = np.max(density_0)

params_figure_main = {
    "density_max":  density_0_max,
    "density_z_eff_max": 400,
    "V_min": -1.0,
    "V_max": 11.0,
    "sigma_z_min": 0.2,
    "sigma_z_max": 0.6,
    "m_atom": m_Rb_87
}

# ---------------------------------------------------------------------------------------------
figure_main = FigureMain(x, y, z, times, params_figure_main)

figure_main.fig_control_inputs.update_u(u_of_times)

figure_main.fig_control_inputs.update_t(0.0)
# ---------------------------------------------------------------------------------------------


# =================================================================================================
# compute time evolution
# =================================================================================================

solver.set_u_of_times(u_of_times)

if export_psi_of_times_analysis:

    psi_of_times_analysis = np.zeros((n_times_analysis, Jx, Jy, Jz), dtype=np.complex128)

else:

    psi_of_times_analysis = None


density_z_eff_of_times_analysis = np.zeros((n_times_analysis, Jz), dtype=np.float64)

phase_z_eff_of_times_analysis = np.zeros((n_times_analysis, Jz), dtype=np.float64)

phase_z_of_times_analysis = np.zeros((n_times_analysis, Jz), dtype=np.float64)

n_inc = n_mod_times_analysis

nr_times_analysis = 0

n = 0

while True:

    t = times[n]

    data = eval_data(solver)

    if export_psi_of_times_analysis:

        psi_of_times_analysis[nr_times_analysis, :] = data.psi

    density_z_eff_of_times_analysis[nr_times_analysis, :] = data.density_z_eff

    phase_z_eff_of_times_analysis[nr_times_analysis, :] = data.phase_z_eff
    phase_z_of_times_analysis[nr_times_analysis, :] = data.phase_z

    print('----------------------------------------------------------------------------------------')
    print('t:             {0:1.2f} / {1:1.2f}'.format(t / 1e-3, times[-1] / 1e-3))
    print('n:             {0:4d} / {1:4d}'.format(n, n_times))
    print()
    print('N:             {0:1.4f}'.format(data.N))
    print('----------------------------------------------------------------------------------------')
    print()

    # ---------------------------------------------------------------------------------------------
    figure_main.update_data(data)

    figure_main.fig_control_inputs.update_t(t)

    figure_main.redraw()

    if export_frames_figure_main:

        filepath = path_frames_figure_main + 'frame_' + str(nr_frame_figure_main).zfill(5) + '.png'

        figure_main.export(filepath)

        nr_frame_figure_main = nr_frame_figure_main + 1
    # ---------------------------------------------------------------------------------------------

    nr_times_analysis = nr_times_analysis + 1

    if n < n_times - n_inc:

        solver.propagate_gpe(n_start=n, n_inc=n_inc, mue_shift=mue_psi_0)

        n = n + n_inc

    else:

        break

    n = n + n_inc


if export_hdf5:

    # ---------------------------------------------------------------------------------------------
    # Create file

    f_hdf5 = h5py.File(filepath_f_hdf5, "w")

    # Create file, fail if exists
    # f_hdf5 = h5py.File(filepath_f_hdf5, "x")
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    f_hdf5.create_dataset("hbar", data=hbar)

    f_hdf5.create_dataset("N", data=N)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    tmp = f_hdf5.create_group("time_evolution")

    if export_psi_of_times_analysis:

        tmp.create_dataset("psi_of_times_analysis", data=psi_of_times_analysis, dtype=np.complex128)

    tmp.create_dataset("density_z_eff_of_times_analysis", data=density_z_eff_of_times_analysis, dtype=np.float64)

    tmp.create_dataset("phase_z_eff_of_times_analysis", data=phase_z_eff_of_times_analysis, dtype=np.float64)
    tmp.create_dataset("phase_z_of_times_analysis", data=phase_z_of_times_analysis, dtype=np.float64)

    tmp.create_dataset("times", data=times)
    tmp.create_dataset("dt", data=dt)
    tmp.create_dataset("n_mod_times_analysis", data=n_mod_times_analysis)

    tmp.create_dataset("times_analysis", data=times_analysis)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    f_hdf5.close()
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    f_hdf5 = h5py.File(filepath_f_hdf5, 'r')

    list_all_items = True

    if list_all_items:

        def print_attrs(name, obj):

            print(name)
            for key, val in obj.attrs.items():
                print("    %s: %s" % (key, val))


        f_hdf5.visititems(print_attrs)

        print()
        print()
    # ---------------------------------------------------------------------------------------------

plt.ioff()
plt.show()
