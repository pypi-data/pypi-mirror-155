import matplotlib.pyplot as plt

from PyQt5 import QtWidgets

from .fig_density_xz_tof_gpe import fig_density_xz_tof_gpe
from .fig_density_xy_tof_gpe import fig_density_xy_tof_gpe

from .fig_density_xz_mask_tof_gpe import fig_density_xz_mask_tof_gpe
from .fig_density_xy_mask_tof_gpe import fig_density_xy_mask_tof_gpe

from .fig_density_xz_tof_final import fig_density_xz_tof_final
from .fig_density_xy_tof_final import fig_density_xy_tof_final

from .. style import colors


class FigureTof(object):

    def __init__(self, x_tof_gpe, y_tof_gpe, z_tof_gpe, x_tof_final, y_tof_final, z_tof_final):

        # -----------------------------------------------------------------------------------------
        x_tof_gpe = x_tof_gpe / 1e-6
        y_tof_gpe = y_tof_gpe / 1e-6
        z_tof_gpe = z_tof_gpe / 1e-6

        dx_tof_gpe = x_tof_gpe[1] - x_tof_gpe[0]
        dy_tof_gpe = y_tof_gpe[1] - y_tof_gpe[0]
        dz_tof_gpe = z_tof_gpe[1] - z_tof_gpe[0]

        Jx_tof_gpe = x_tof_gpe.size
        Jy_tof_gpe = y_tof_gpe.size
        Jz_tof_gpe = z_tof_gpe.size

        x_min_tof_gpe = x_tof_gpe[0]
        x_max_tof_gpe = x_min_tof_gpe + Jx_tof_gpe * dx_tof_gpe

        y_min_tof_gpe = y_tof_gpe[0]
        y_max_tof_gpe = y_min_tof_gpe + Jy_tof_gpe * dy_tof_gpe

        z_min_tof_gpe = z_tof_gpe[0]
        z_max_tof_gpe = z_min_tof_gpe + Jz_tof_gpe * dz_tof_gpe
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        x_tof_final = x_tof_final / 1e-6
        y_tof_final = y_tof_final / 1e-6
        z_tof_final = z_tof_final / 1e-6

        Jx_tof_final = x_tof_final.size
        Jy_tof_final = y_tof_final.size
        Jz_tof_final = z_tof_final.size

        x_min_tof_final = x_tof_final[0]
        x_max_tof_final = x_tof_final[-1]

        y_min_tof_final = y_tof_final[0]
        y_max_tof_final = y_tof_final[-1]

        z_min_tof_final = z_tof_final[0]
        z_max_tof_final = z_tof_final[-1]
        # -----------------------------------------------------------------------------------------

        # =========================================================================================
        # -----------------------------------------------------------------------------------------
        settings = type('', (), {})()
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        settings.x_min_tof_gpe = x_min_tof_gpe
        settings.x_max_tof_gpe = x_max_tof_gpe

        settings.y_min_tof_gpe = y_min_tof_gpe
        settings.y_max_tof_gpe = y_max_tof_gpe

        settings.z_min_tof_gpe = z_min_tof_gpe
        settings.z_max_tof_gpe = z_max_tof_gpe

        settings.Jx_tof_gpe = Jx_tof_gpe
        settings.Jy_tof_gpe = Jy_tof_gpe
        settings.Jz_tof_gpe = Jz_tof_gpe
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        settings.x_min_tof_final = x_min_tof_final
        settings.x_max_tof_final = x_max_tof_final

        settings.y_min_tof_final = y_min_tof_final
        settings.y_max_tof_final = y_max_tof_final

        settings.z_min_tof_final = z_min_tof_final
        settings.z_max_tof_final = z_max_tof_final

        settings.Jx_tof_final = Jx_tof_final
        settings.Jy_tof_final = Jy_tof_final
        settings.Jz_tof_final = Jz_tof_final
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        settings.cmap_density = colors.colormap_1
        settings.cmap_density_mask = colors.cmap_black_white

        settings.cmap_spectrum_abs = colors.colormap_1
        settings.cmap_spectrum_abs_mask = colors.cmap_black_white
        # -----------------------------------------------------------------------------------------
        # =========================================================================================

        # -----------------------------------------------------------------------------------------
        plt.rcParams.update({'font.size': 10})
        # -----------------------------------------------------------------------------------------

        # =========================================================================================
        # -----------------------------------------------------------------------------------------
        self.fig_name = "figure_time_of_flight"

        self.fig = plt.figure(self.fig_name, facecolor="white")

        window = self.fig.canvas.window()

        window.findChild(QtWidgets.QToolBar).setVisible(False)

        window.statusBar().setVisible(False)
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        n_pixels_x = 800
        n_pixels_y = 600

        pos_x = 2560 - n_pixels_x
        pos_y = 0

        window.setGeometry(pos_x, pos_y, n_pixels_x, n_pixels_y)
        # -----------------------------------------------------------------------------------------
        # =========================================================================================

        # -----------------------------------------------------------------------------------------
        gridspec = self.fig.add_gridspec(nrows=2, ncols=3,
                                         left=0.1, right=0.95,
                                         bottom=0.1, top=0.925,
                                         wspace=0.4, hspace=0.35,
                                         width_ratios=[1, 1, 1],
                                         height_ratios=[1, 1])

        ax_00 = self.fig.add_subplot(gridspec[0, 0])
        ax_10 = self.fig.add_subplot(gridspec[1, 0])

        ax_01 = self.fig.add_subplot(gridspec[0, 1])
        ax_11 = self.fig.add_subplot(gridspec[1, 1])

        ax_02 = self.fig.add_subplot(gridspec[0, 2])
        ax_12 = self.fig.add_subplot(gridspec[1, 2])
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        self.fig_density_xz_tof_gpe = fig_density_xz_tof_gpe(ax_00, settings)
        self.fig_density_xy_tof_gpe = fig_density_xy_tof_gpe(ax_10, settings)

        self.fig_density_xz_mask_tof_gpe = fig_density_xz_mask_tof_gpe(ax_01, settings)
        self.fig_density_xy_mask_tof_gpe = fig_density_xy_mask_tof_gpe(ax_11, settings)

        self.fig_density_xz_tof_final = fig_density_xz_tof_final(ax_02, settings)
        self.fig_density_xy_tof_final = fig_density_xy_tof_final(ax_12, settings)
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        plt.ion()
        
        plt.draw()
        plt.pause(0.001)
        # -----------------------------------------------------------------------------------------

    def update_data(self, data_tof):

        # -----------------------------------------------------------------------------------------
        self.fig_density_xz_tof_gpe.update(data_tof.density_xz_tof_gpe)
        self.fig_density_xy_tof_gpe.update(data_tof.density_xy_tof_gpe)

        self.fig_density_xz_mask_tof_gpe.update(data_tof.density_xz_mask_tof_gpe)
        self.fig_density_xy_mask_tof_gpe.update(data_tof.density_xy_mask_tof_gpe)

        self.fig_density_xz_tof_final.update(data_tof.density_xz_tof_final)
        self.fig_density_xy_tof_final.update(data_tof.density_xy_tof_final)
        # -----------------------------------------------------------------------------------------

        # -----------------------------------------------------------------------------------------
        plt.figure(self.fig_name)
        
        plt.draw()
        
        self.fig.canvas.start_event_loop(0.001)
        # -----------------------------------------------------------------------------------------

    def export(self, filepath):

        # -----------------------------------------------------------------------------------------
        plt.figure(self.fig_name)

        plt.draw()

        self.fig.canvas.start_event_loop(0.001)
        # -----------------------------------------------------------------------------------------

        plt.savefig(filepath,
                    dpi=None,
                    facecolor='w',
                    edgecolor='w',
                    format='png',
                    transparent=False,
                    bbox_inches=None,
                    pad_inches=0,
                    metadata=None)
