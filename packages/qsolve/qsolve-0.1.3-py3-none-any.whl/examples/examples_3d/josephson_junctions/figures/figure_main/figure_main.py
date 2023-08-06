import matplotlib.pyplot as plt

from PyQt5 import QtWidgets

from scipy import constants

import numpy as np

from .fig_density_xz import fig_density_xz
from .fig_density_xy import fig_density_xy

from .fig_density_x import fig_density_x
from .fig_density_y import fig_density_y
from .fig_density_z import fig_density_z

from .fig_phase_difference_xz import fig_phase_difference_xz
from .fig_phase_difference_xy import fig_phase_difference_xy

from .fig_phase_difference_z_x1_x2 import fig_phase_difference_z_x1_x2

from .fig_control_inputs import fig_control_inputs

from .fig_global_phase_difference import fig_global_phase_difference

from .fig_number_imbalance import fig_number_imbalance

from .. style import colors


class FigureMain(object):

    def __init__(self, x, y, z, times, params):

        hbar = constants.hbar

        m_atom = params['m_atom']

        density_min = -0.2 * params["density_max"]
        density_max = +1.2 * params["density_max"]

        V_min = params['V_min']
        V_max = params['V_max']

        abs_z_restr = params['abs_z_restr'] / 1e-6

        x = x / 1e-6
        y = y / 1e-6
        z = z / 1e-6

        indices_z_restr = np.abs(z) < abs_z_restr

        times = times / 1e-3

        Jx = x.shape[0]
        Jy = y.shape[0]
        Jz = z.shape[0]

        dx = x[1] - x[0]
        dy = y[1] - y[0]
        dz = z[1] - z[0]

        x_min = x[0]
        y_min = y[0]
        z_min = z[0]

        x_max = x_min + Jx * dx
        y_max = y_min + Jy * dy
        z_max = z_min + Jz * dz
        
        t_min = times[0]
        t_max = times[-1]

        Jx = x.size
        Jy = y.size
        Jz = z.size

        x_ticks = np.array([-2, -1, 0, 1, 2])

        y_ticks = np.array([-1, 0, 1])

        # -----------------------------------------------------------------------------------------
        if np.round(z_max) == 5:

            z_ticks = np.array([-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])

        elif np.round(z_max) == 10:

            z_ticks = np.array([-10, -5, 0, 5, 10])

        elif np.round(z_max) == 20:

            z_ticks = np.array([-20, -10, 0, 10, 20])

        elif np.round(z_max) == 40:

            z_ticks = np.array([-40, -30, -20, -10, 0, 10, 20, 30, 40])

        elif np.round(z_max) == 50:

            z_ticks = np.array([-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50])

        elif np.round(z_max) == 60:

            z_ticks = np.array([-60, -40, -20, 0, 20, 40, 60])

        elif np.round(z_max) == 80:

            z_ticks = np.array([-80, -60, -40, -20, 0, 20, 40, 60, 80])

        elif np.round(z_max) == 100:

            z_ticks = np.array([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100])

        elif np.round(z_max) == 200:

            z_ticks = np.array([-200, -160, -120, -80, -40, 0, 40, 80, 120, 160, 200])

        else:

            z_ticks = np.array([z_min, z_max])
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        if t_max == 2:

            t_ticks_major = np.array([0, 1, 2])

        elif t_max == 2.5:

            t_ticks_major = np.array([0, 0.5, 1, 1.5, 2, 2.5])

        elif t_max == 4:

            t_ticks_major = np.array([0, 1, 2, 3, 4])

        elif t_max == 5:

            t_ticks_major = np.array([0, 1, 2, 3, 4, 5])

        elif t_max == 8:

            t_ticks_major = np.array([0, 2, 4, 6, 8])

        elif t_max == 10:

            t_ticks_major = np.array([0, 2, 4, 6, 8, 10])

        elif t_max == 20:

            t_ticks_major = np.array([0, 4, 8, 12, 16, 20])

        elif t_max == 40:

            t_ticks_major = np.array([0, 10, 20, 30, 40])

        elif t_max == 80:

            t_ticks_major = np.array([0, 20, 40, 60, 80])

        elif t_max == 160:

            t_ticks_major = np.array([0, 40, 80, 120, 160])

        elif t_max == 200:

            t_ticks_major = np.array([0, 40, 80, 120, 160, 200])

        else:

            t_ticks_major = np.array([0, t_max])
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        t_ticks_minor = 0.5 * (t_ticks_major[0:-1] + t_ticks_major[1:])
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        settings = type('', (), {})()

        settings.hbar = hbar
        settings.m_atom = m_atom

        settings.density_min = density_min
        settings.density_max = density_max

        settings.V_min = V_min
        settings.V_max = V_max

        settings.indices_z_restr = indices_z_restr

        settings.x = x
        settings.y = y
        settings.z = z

        settings.Jx = Jx
        settings.Jy = Jy
        settings.Jz = Jz

        settings.x_ticks = x_ticks
        settings.y_ticks = y_ticks
        settings.z_ticks = z_ticks

        settings.x_min = x_min
        settings.x_max = x_max

        settings.y_min = y_min
        settings.y_max = y_max

        settings.z_min = z_min
        settings.z_max = z_max

        settings.times = times

        settings.t_min = t_min
        settings.t_max = t_max

        settings.t_ticks_major = t_ticks_major
        settings.t_ticks_minor = t_ticks_minor

        settings.label_V = r'$V \;\, \mathrm{in} \;\, h \times \mathrm{kHz}$'

        settings.label_density = r'$\mathrm{density} \;\, \mathrm{in} \;\, \mathrm{m}^{-3}$'
        settings.label_density_effective = r'$\mathrm{density} \;\, \mathrm{in} \;\, \mu \mathrm{m}^{-1}$'

        settings.label_x = r'$x \;\, \mathrm{in} \;\, \mu \mathrm{m}$'
        settings.label_y = r'$y \;\, \mathrm{in} \;\, \mu \mathrm{m}$'
        settings.label_z = r'$z \;\, \mathrm{in} \;\, \mu \mathrm{m}$'

        settings.label_t = r'$t \;\, \mathrm{in} \;\, \mathrm{ms}$'

        # settings.cmap_density = plt.get_cmap('CMRmap')
        settings.cmap_density = colors.colormap_1

        settings.cmap_phase = plt.get_cmap('PRGn')
        # settings.cmap_phase = colors.colormap_2

        settings.color_gridlines_major = colors.color_gridlines_major
        settings.color_gridlines_minor = colors.color_gridlines_minor

        settings.framealpha = 1.0
        settings.fancybox = False

        settings.fontsize_titles = 10
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        plt.rcParams.update({'font.size': 10})
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        self.fig_name = "figure_main"
                
        self.fig = plt.figure(self.fig_name, facecolor="white")

        window = self.fig.canvas.window()
        
        window.findChild(QtWidgets.QToolBar).setVisible(False)
        window.statusBar().setVisible(False)
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        n_pixels_x = 1600
        n_pixels_y = 800

        pos_x = 2560 - n_pixels_x
        pos_y = 0

        window.setGeometry(pos_x, pos_y, n_pixels_x, n_pixels_y)
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        self.gridspec = self.fig.add_gridspec(nrows=4, ncols=4,
                                              left=0.055, right=0.985,
                                              bottom=0.08, top=0.95,
                                              wspace=0.5,
                                              hspace=0.7,
                                              width_ratios=[3, 1, 1, 2.5],
                                              height_ratios=[1, 1, 1, 1])

        ax_00 = self.fig.add_subplot(self.gridspec[0, 0])
        ax_01 = self.fig.add_subplot(self.gridspec[0, 1])

        ax_03 = self.fig.add_subplot(self.gridspec[0, 3])

        ax_10 = self.fig.add_subplot(self.gridspec[1, 0])
        ax_11 = self.fig.add_subplot(self.gridspec[1, 1])
        ax_12 = self.fig.add_subplot(self.gridspec[1, 2])

        ax_13 = self.fig.add_subplot(self.gridspec[1, 3])

        ax_20 = self.fig.add_subplot(self.gridspec[2, 0])
        ax_21 = self.fig.add_subplot(self.gridspec[2, 1])

        ax_23 = self.fig.add_subplot(self.gridspec[2, 3])

        ax_30 = self.fig.add_subplot(self.gridspec[3, 0])
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        self.fig_density_xz = fig_density_xz(ax_00, settings)
        self.fig_density_xy = fig_density_xy(ax_01, settings)

        self.fig_density_z = fig_density_z(ax_10, settings)
        self.fig_density_y = fig_density_y(ax_11, settings)
        self.fig_density_x = fig_density_x(ax_12, settings)

        self.fig_phase_difference_xz = fig_phase_difference_xz(ax_20, settings)
        self.fig_phase_difference_xy = fig_phase_difference_xy(ax_21, settings)

        self.fig_phase_difference_z_x1_x2 = fig_phase_difference_z_x1_x2(ax_30, settings)

        self.fig_control_inputs = fig_control_inputs(ax_03, settings)

        self.fig_global_phase_difference = fig_global_phase_difference(ax_13, settings)

        self.fig_number_imbalance = fig_number_imbalance(ax_23, settings)
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        plt.ion()
        
        plt.draw()
        plt.pause(0.001)
        # -----------------------------------------------------------------------------------------

    def update_data(self, data):

        self.fig_density_xz.update(data.density_xz)
        self.fig_density_xy.update(data.density_xy)

        self.fig_density_z.update(data.density_z_x1, data.density_z_x2, data.V_z_x1)
        self.fig_density_y.update(data.density_y_x1, data.V_y_x1)
        self.fig_density_x.update(data.density_x, data.V_x)

        self.fig_phase_difference_xz.update(data.phase_difference_xz)
        self.fig_phase_difference_xy.update(data.phase_difference_xy)

        self.fig_phase_difference_z_x1_x2.update(data.phase_difference_z_x1_x2)

    def update_data_time_evolution(self, data_time_evolution):

        global_phase_difference_of_times_analysis = data_time_evolution.global_phase_difference_of_times_analysis
        number_imbalance_of_times_analysis = data_time_evolution.number_imbalance_of_times_analysis

        times_analysis = data_time_evolution.times_analysis

        nr_times_analysis = data_time_evolution.nr_times_analysis

        self.fig_global_phase_difference.update(global_phase_difference_of_times_analysis,
                                                times_analysis,
                                                nr_times_analysis)

        self.fig_number_imbalance.update(number_imbalance_of_times_analysis,
                                         times_analysis,
                                         nr_times_analysis)

    def redraw(self):

        plt.figure(self.fig_name)

        plt.draw()

        self.fig.canvas.start_event_loop(0.001)

    def export(self, filepath):

        plt.figure(self.fig_name)

        plt.draw()

        self.fig.canvas.start_event_loop(0.001)

        plt.savefig(filepath,
                    dpi=None,
                    facecolor='w',
                    edgecolor='w',
                    format='png',
                    transparent=False,
                    bbox_inches=None,
                    pad_inches=0,
                    metadata=None)
