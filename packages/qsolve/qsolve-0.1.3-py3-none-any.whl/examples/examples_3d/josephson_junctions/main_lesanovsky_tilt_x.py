from qsolve.solvers.solvers_3d.solver_gpe_3d import SolverGPE3D

import mkl

import os

import h5py

import numpy as np

from scipy import constants

import matplotlib.pyplot as plt

from figures.figure_main.figure_main import FigureMain
from figures.figure_tof.figure_tof import FigureTof
from figures.figure_tof_extended.figure_tof_extended import FigureTofExtended

from evaluation import eval_data
from evaluation import eval_data_tof

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

quickstart = False

visualization = True

time_of_flight = False
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
export_frames_figure_main = False
export_frames_figure_tof = False

export_hdf5 = False

export_psi_of_times_analysis = False
# -------------------------------------------------------------------------------------------------


# =================================================================================================
N = 3500

u1_final = 0.56

if quickstart:

    gamma_tilt_ref = 0.0

    # xi_ext = 0.420
    xi_ext = 0.350

else:

    gamma_tilt_ref = 4.1e-26

    xi_ext = 0.0


t_final = 80e-3

if temperature:

    T = 20e-9

else:

    T = 0e-9

m_Rb_87 = 87 * amu

m_atom = m_Rb_87

a_s = 5.24e-9

Jx = 2 * 28
Jy = 2 * 12
Jz = 4 * 60

dt = 0.0025e-3

n_mod_times_analysis = 100

x_min = -2.8e-6
x_max = +2.8e-6

y_min = -1.2e-6
y_max = +1.2e-6

z_min = -60e-6
z_max = +60e-6

params_potential = {
    "name": 'lesanovsky_tilt_x',
    "g_F": -1/2,
    "m_F": -1,
    "m_F_prime": -1,
    "omega_perp": 2 * np.pi * 3e3,
    "omega_para": 2 * np.pi * 22.5,
    "omega_delta_detuning": -2 * np.pi * 50e3,
    "omega_trap_bottom": 2 * np.pi * 1216e3,
    "omega_rabi_ref": 2 * np.pi * 575e3,
    "gamma_tilt_ref": gamma_tilt_ref
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

assert (times_analysis[-1] == t_final)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
times_tof = times_analysis.copy()

indices_tmp = times_analysis >= 21.5e-3

times_tof = times_tof[indices_tmp]
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# init control inputs
# =================================================================================================

if quickstart:

    t_idle = 5e-3

    t_phase_imprint_part_1 = 1.5e-3
    t_phase_imprint_part_2 = 1.5e-3

    t0 = 0.0
    t1 = t0 + t_idle
    t2 = t1 + t_phase_imprint_part_1
    t3 = t2 + t_phase_imprint_part_2

    vec_t = np.array([t0, t1, t2, t3])

    vec_u2 = np.array([0, 0, 1, 0])

    u1_of_times = u1_final * np.ones_like(times)

    # u2_of_times = np.interp(times, vec_t, vec_u2)

    u2_of_times = np.zeros_like(times)

else:

    t_ramp_up = 21.5e-3

    t_phase_imprint_part_1 = 1.5e-3
    t_phase_imprint_part_2 = 1.5e-3
    t_ramp_down = 3.0e-3
    t_help = 10.0e-3

    t0 = 0.0
    t1 = t0 + t_ramp_up
    t2 = t1 + t_phase_imprint_part_1
    t3 = t2 + t_phase_imprint_part_2
    t4 = t3 + t_ramp_down
    t5 = t4 + t_help

    u1_0 = 0.0
    u1_1 = 0.65
    u1_2 = 0.65
    u1_3 = 0.65
    u1_4 = u1_final
    u1_5 = u1_final

    vec_t = np.array([t0, t1, t2, t3, t4, t5])

    vec_u1 = np.array([u1_0, u1_1, u1_2, u1_3, u1_4, u1_5])
    vec_u2 = np.array([0, 0, 1, 0, 0, 0])

    u1_of_times = np.interp(times, vec_t, vec_u1)
    u2_of_times = np.interp(times, vec_t, vec_u2)

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

if visualization:

    # ---------------------------------------------------------------------------------------------
    figure_main = FigureMain(x, y, z, times, params_figure_main)

    figure_main.fig_control_inputs.update_u(u1_of_times, u2_of_times)

    figure_main.fig_control_inputs.update_t(0.0)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    data = eval_data(solver)

    figure_main.update_data(data)

    figure_main.redraw()
    # ---------------------------------------------------------------------------------------------

else:

    figure_main = None


# =================================================================================================
# thermal state sampling
# =================================================================================================

if T > 0:

    solver.init_sgpe_z_eff(
        T_temp_des=T,
        mue_des=mue_psi_0,
        gamma=0.1,
        dt=dt,
        filter_z1=-45e-6,
        filter_z2=+45e-6,
        filter_z_s=1.0e-6
    )

    n_sgpe_max = 10000

    n_sgpe_inc = 1000

    n_sgpe = 0

    while n_sgpe < n_sgpe_max:

        data = eval_data(solver)

        print('----------------------------------------------------------------------------------------')
        print('n_sgpe: {0:4d} / {1:4d}'.format(n_sgpe, n_sgpe_max))
        print()
        print('N:      {0:1.4f}'.format(data.N))
        print('----------------------------------------------------------------------------------------')
        print()

        if visualization:

            # -----------------------------------------------------------------------------------------
            figure_main.update_data(data)

            figure_main.redraw()
            # -----------------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------------
        # apply thermal state sampling process via sgpe for n_sgpe_inc time steps

        solver.propagate_sgpe_z_eff(n_inc=n_sgpe_inc)
        # ---------------------------------------------------------------------------------------------

        n_sgpe = n_sgpe + n_sgpe_inc


# =================================================================================================
# imprint relative phase difference by hand
# =================================================================================================

if quickstart:

    psi = solver.get('psi')

    x = solver.get('x')

    phi_ext = 1.1 * xi_ext * pi

    s0 = 0.125e-6

    phase_shift_x = (0.5 * phi_ext) * (2 * np.arctan(x / s0) / pi)

    visualize_phase_shift_x = True

    if visualize_phase_shift_x:

        fig_phase_shift_x = plt.figure("figure_phase_shift_x", figsize=(6, 5), facecolor="white")

        plt.plot(x / 1e-6, phase_shift_x / pi, linewidth=1, linestyle='-', color='k')

        plt.xlim([1.05 * x_min / 1e-6, 1.05 * x_max / 1e-6])
        plt.ylim([-0.4, 0.4])

        plt.xlabel(r'$x$ in $\mu$m')
        plt.ylabel(r'$\phi\; / \;\pi$')

        plt.grid(b=True, which='major', color='k', linestyle='-', linewidth=0.5)

    phase_shift = phase_shift_x[:, np.newaxis, np.newaxis]

    psi = np.exp(-1j * phase_shift) * psi

    solver.set_psi('numpy', array=psi)


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

if time_of_flight:

    solver.init_time_of_flight(params_tof)

    x_tof_gpe = solver.get('x_tof_free_gpe')
    y_tof_gpe = solver.get('y_tof_free_gpe')
    z_tof_gpe = solver.get('z_tof_free_gpe')

    x_tof_final = solver.get('x_tof_final')
    y_tof_final = solver.get('y_tof_final')
    z_tof_final = solver.get('z_tof_final')

    figure_tof = FigureTof(x_tof_gpe, y_tof_gpe, z_tof_gpe, x_tof_final, y_tof_final, z_tof_final)
    # figure_tof = FigureTofExtended(x_tof_gpe, y_tof_gpe, z_tof_gpe, x_tof_final, y_tof_final, z_tof_final)

else:

    figure_tof = None

while True:

    t = times[n]

    data = eval_data(solver)

    if export_psi_of_times_analysis:

        data_time_evolution.psi_of_times_analysis[nr_times_analysis, :] = data.psi

    data_time_evolution.global_phase_difference_of_times_analysis[nr_times_analysis] = data.global_phase_difference
    data_time_evolution.number_imbalance_of_times_analysis[nr_times_analysis] = data.number_imbalance

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

        figure_main.update_data_time_evolution(data_time_evolution)

        figure_main.fig_control_inputs.update_t(t)

        figure_main.redraw()

        if export_frames_figure_main:

            filepath = path_frames_figure_main + 'frame_' + str(nr_frame_figure_main).zfill(5) + '.png'

            figure_main.export(filepath)

            nr_frame_figure_main = nr_frame_figure_main + 1
        # -----------------------------------------------------------------------------------------

    if time_of_flight:

        if t in times_tof:

            solver.compute_time_of_flight()

            data_tof = eval_data_tof(solver)

            figure_tof.update_data(data_tof)

            if export_frames_figure_tof:

                filepath = path_frames_figure_tof + 'frame_' + str(nr_frame_figure_tof).zfill(5) + '.png'

                figure_tof.export(filepath)

                nr_frame_figure_tof = nr_frame_figure_tof + 1

    nr_times_analysis = nr_times_analysis + 1

    if n < n_times - n_inc:

        solver.propagate_gpe(n_start=n, n_inc=n_inc, mue_shift=mue_psi_0)

        n = n + n_inc

    else:

        break

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

    f_hdf5.create_dataset("x", data=x)
    f_hdf5.create_dataset("y", data=y)
    f_hdf5.create_dataset("z", data=z)

    f_hdf5.create_dataset("Jz", data=Jz)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    tmp = f_hdf5.create_group("time_evolution")

    if export_psi_of_times_analysis:

        tmp.create_dataset("psi_of_times_analysis", data=data_time_evolution.psi_of_times_analysis, dtype=np.complex128)

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
