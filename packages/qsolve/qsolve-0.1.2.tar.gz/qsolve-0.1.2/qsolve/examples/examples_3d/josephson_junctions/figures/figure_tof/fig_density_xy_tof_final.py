import numpy as np


class fig_density_xy_tof_final(object):

    def __init__(self, ax, settings):

        ax.set_title('density (final)')

        ax.set_xlabel(r'$x$')
        ax.set_ylabel(r'$y$')

        ax.set_xlim([settings.x_min_tof_final, settings.x_max_tof_final])
        ax.set_ylim([settings.y_min_tof_final, settings.y_max_tof_final])

        ax.set_xticks([settings.x_min_tof_final, 0, settings.x_max_tof_final])
        ax.set_yticks([settings.y_min_tof_final, 0, settings.y_max_tof_final])

        density_xy_tof_final = np.zeros((settings.Jx_tof_final, settings.Jy_tof_final))

        left = settings.x_min_tof_final
        right = settings.x_max_tof_final

        bottom = settings.y_min_tof_final
        top = settings.y_max_tof_final

        self.image_density_xy_tof_final = ax.imshow(
            np.transpose(density_xy_tof_final),
            extent=[left, right, bottom, top],
            cmap=settings.cmap_density,
            aspect='auto',
            interpolation='bilinear',
            vmin=0,
            vmax=1,
            origin='lower')

    def update(self, density_xy_tof_final):

        self.image_density_xy_tof_final.set_data(np.transpose(density_xy_tof_final))
