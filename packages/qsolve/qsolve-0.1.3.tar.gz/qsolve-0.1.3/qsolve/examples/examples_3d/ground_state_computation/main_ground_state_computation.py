from qsolve.solvers.solvers_3d.solver_gpe_3d import SolverGPE3D

import mkl

import os

import numpy as np

from scipy import constants

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
temperature = True

visualization = True

time_of_flight = True
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
export_frames_figure_main = False
export_frames_figure_tof = False

export_hdf5 = False

export_psi_of_times_analysis = False
# -------------------------------------------------------------------------------------------------


# =================================================================================================
N = 3500

m_Rb_87 = 87 * amu

m_atom = m_Rb_87

a_s = 5.24e-9

x_min = -5e-6
x_max = +5e-6

y_min = -5e-6
y_max = +5e-6

z_min = -10e-6
z_max = +10e-6

Jx = 50
Jy = 50
Jz = 100

t_final = 4e-3

dt = 0.001e-3

n_mod_times_analysis = 100

params_potential = {
    "name": 'harmonic',
    "omega_x": 2 * np.pi * 200,
    "omega_y": 2 * np.pi * 100,
    "omega_z": 2 * np.pi * 50
}

params_figure_main = {
    'm_atom': m_atom,
    'density_min': -0.2e20,
    'density_max': +2.2e20,
    'V_min': -1.0,
    'V_max': 11.0,
    'abs_z_restr': 30e-6
}
# =================================================================================================

# =================================================================================================
times_tof = 1e-3 * np.array([21.5, 24.5, 27.5, 28, 28.5, 29, 29.5, 30, 30.5, 31, 32.5, 33, 33.5, 34, 34.5, 35,
                             40, 50, 60, 70, 80])

# -------------------------------------------------------------------------------------------------
T_tof_total = 20e-3
T_tof_free_gpe = 1e-3
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
Jx_tof_free_gpe = 300
Jy_tof_free_gpe = 300
Jz_tof_free_gpe = 300
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
x_min_tof_final = -100e-6
x_max_tof_final = +100e-6

y_min_tof_final = -100e-6
y_max_tof_final = +100e-6

z_min_tof_final = -75e-6
z_max_tof_final = +75e-6

Jx_tof_final = 101
Jy_tof_final = 101
Jz_tof_final = 101
# -------------------------------------------------------------------------------------------------

params_tof = {
    "Jx_tof_free_gpe": Jx_tof_free_gpe,
    "Jy_tof_free_gpe": Jy_tof_free_gpe,
    "Jz_tof_free_gpe": Jz_tof_free_gpe,
    "x_min_tof_final": x_min_tof_final,
    "y_min_tof_final": y_min_tof_final,
    "z_min_tof_final": z_min_tof_final,
    "x_max_tof_final": x_max_tof_final,
    "y_max_tof_final": y_max_tof_final,
    "z_max_tof_final": z_max_tof_final,
    "Jx_tof_final": Jx_tof_final,
    "Jy_tof_final": Jy_tof_final,
    "Jz_tof_final": Jz_tof_final,
    "T_tof_free_gpe": T_tof_free_gpe,
    "T_tof_total": T_tof_total
}
# =================================================================================================

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
path_frames_figure_tof = "./frames/frames_figure_tof/" + simulation_id + "/"

nr_frame_figure_main = 0
nr_frame_figure_tof = 0

if export_frames_figure_main:

    if not os.path.exists(path_frames_figure_main):

        os.makedirs(path_frames_figure_main)

if export_frames_figure_tof:

    if not os.path.exists(path_frames_figure_tof):

        os.makedirs(path_frames_figure_tof)
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# init solver and its potential
# =================================================================================================

solver = SolverGPE3D(m_atom=m_Rb_87,
                     a_s=a_s,
                     seed=1,
                     device='cuda:0',
                     num_threads=num_threads_cpu)

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

# -------------------------------------------------------------------------------------------------
solver.init_time_evolution(t_final=t_final, dt=dt)

times = solver.get('times')

n_times = times.size
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
times_analysis = times[0::n_mod_times_analysis]

n_times_analysis = times_analysis.size

assert (abs(times_analysis[-1] - t_final) < 1e-14)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
times_tof = times_analysis.copy()

indices_tmp = times_analysis >= 21.5e-3

times_tof = times_tof[indices_tmp]
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# init control inputs
# =================================================================================================

u1_of_times = np.ones_like(times)
u2_of_times = np.ones_like(times)

u_of_times = np.zeros((2, n_times))

u_of_times[0, :] = u1_of_times
u_of_times[1, :] = u2_of_times


# =================================================================================================
# compute ground state solution psi_0
# =================================================================================================

# -------------------------------------------------------------------------------------------------
u1_0 = u1_of_times[0]
u2_0 = u2_of_times[0]

solver.set_V(u=[u1_0, u2_0])
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
solver.compute_ground_state_solution(N=N, n_iter=5000, tau=0.005e-3, adaptive_tau=True)

psi_0 = solver.get('psi_0')

N_psi_0 = solver.compute_n_atoms('psi_0')
mue_psi_0 = solver.compute_chemical_potential('psi_0')
E_psi_0 = solver.compute_E_total('psi_0')

vec_res = solver.get('vec_res_ground_state_computation')
vec_iter = solver.get('vec_iter_ground_state_computation')

print('N_psi_0 = {:1.16e}'.format(N_psi_0))
print('mue_psi_0 / h: {0:1.6} kHz'.format(mue_psi_0 / (1e3 * (2 * pi * hbar))))
print('E_psi_0 / (N_psi_0*h): {0:1.6} kHz'.format(E_psi_0 / (1e3 * (2 * pi * hbar * N_psi_0))))
print()
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# set wave function psi to ground state solution psi_0
# =================================================================================================

solver.set_psi('numpy', array=psi_0)


# =================================================================================================
# init figure
# =================================================================================================

# -------------------------------------------------------------------------------------------------
figure_main = FigureMain(x, y, z, times, params_figure_main)

figure_main.fig_control_inputs.update_u(u1_of_times, u2_of_times)

figure_main.fig_control_inputs.update_t(0.0)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
data = eval_data(solver)

figure_main.update_data(data)

figure_main.redraw()
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
fig = plt.figure("figure_residual_error", figsize=(6, 5), facecolor="white")

gridspec = fig.add_gridspec(
        nrows=1, ncols=1,
        left=0.175, right=0.95,
        bottom=0.125, top=0.95,
        wspace=0.5,
        hspace=0.7,
        width_ratios=[1],
        height_ratios=[1])

ax_00 = fig.add_subplot(gridspec[0, 0])

ax_00.set_yscale('log')

x_values = vec_iter[1:]
y_values = vec_res[1:]

plt.plot(x_values, y_values, linewidth=1, linestyle='-', color='k')

ax_00.set_xlim(0, 1.1 * x_values[-1])
ax_00.set_ylim(1e-8, 1)

plt.xlabel(r'number of iterations')
plt.ylabel(r'relative residual error')

plt.grid(visible=True, which='major', color='k', linestyle='-', linewidth=0.5)
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# compute time evolution
# =================================================================================================

solver.set_u_of_times(u_of_times)

# -------------------------------------------------------------------------------------------------
data_time_evolution = type('', (), {})()

if export_psi_of_times_analysis:

    data_time_evolution.psi_of_times_analysis = np.zeros((n_times_analysis, Jx, Jy, Jz), dtype=np.complex128)

else:

    data_time_evolution.psi_of_times_analysis = None

data_time_evolution.global_phase_difference_of_times_analysis = np.zeros((n_times_analysis,), dtype=np.float64)
data_time_evolution.number_imbalance_of_times_analysis = np.zeros((n_times_analysis,), dtype=np.float64)

data_time_evolution.times_analysis = times_analysis
# -------------------------------------------------------------------------------------------------

n_inc = n_mod_times_analysis

nr_times_analysis = 0

stop = False

n = 0

while True:

    t = times[n]

    data = eval_data(solver)

    if export_psi_of_times_analysis:

        data_time_evolution.psi_of_times_analysis[nr_times_analysis, :] = data.psi

    # data_time_evolution.global_phase_difference_of_times_analysis[nr_times_analysis] = data.global_phase_difference
    # data_time_evolution.number_imbalance_of_times_analysis[nr_times_analysis] = data.number_imbalance

    data_time_evolution.nr_times_analysis = nr_times_analysis

    print('----------------------------------------------------------------------------------------')
    print('t: {0:1.2f} / {1:1.2f}'.format(t / 1e-3, times[-1] / 1e-3))
    print('n: {0:4d} / {1:4d}'.format(n, n_times))
    print()
    print('N: {0:1.4f}'.format(data.N))
    print('----------------------------------------------------------------------------------------')
    print()

    if visualization:

        # -----------------------------------------------------------------------------------------
        figure_main.update_data(data)

        # figure_main.update_data_time_evolution(data_time_evolution)

        figure_main.fig_control_inputs.update_t(t)

        figure_main.redraw()

        if export_frames_figure_main:

            filepath = path_frames_figure_main + 'frame_' + str(nr_frame_figure_main).zfill(5) + '.png'

            figure_main.export(filepath)

            nr_frame_figure_main = nr_frame_figure_main + 1
        # -----------------------------------------------------------------------------------------

    nr_times_analysis = nr_times_analysis + 1

    if n < n_times - n_inc:

        # solver.propagate_gpe(n_start=n, n_inc=n_inc, mue_shift=mue_psi_0)
        solver.propagate_gpe(n_start=n, n_inc=n_inc, mue_shift=0.0)

        n = n + n_inc

    else:

        break


plt.ioff()
plt.show()
