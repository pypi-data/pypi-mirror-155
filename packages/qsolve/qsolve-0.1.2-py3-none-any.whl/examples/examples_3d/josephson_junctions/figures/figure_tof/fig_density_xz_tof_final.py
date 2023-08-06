import numpy as np


class fig_density_xz_tof_final(object):

    def __init__(self, ax, settings):

        ax.set_title('density (final)')

        ax.set_xlabel(r'$x$')
        ax.set_ylabel(r'$z$')

        ax.set_xlim([settings.x_min_tof_final, settings.x_max_tof_final])
        ax.set_ylim([settings.z_min_tof_final, settings.z_max_tof_final])

        ax.set_xticks([settings.x_min_tof_final, 0, settings.x_max_tof_final])
        ax.set_yticks([settings.z_min_tof_final, 0, settings.z_max_tof_final])

        density_xz_tof_final = np.zeros((settings.Jx_tof_final, settings.Jz_tof_final))

        left = settings.x_min_tof_final
        right = settings.x_max_tof_final

        bottom = settings.z_min_tof_final
        top = settings.z_max_tof_final

        self.image_density_xz_tof_final = ax.imshow(
            np.transpose(density_xz_tof_final),
            extent=[left, right, bottom, top],
            cmap=settings.cmap_density,
            aspect='auto',
            interpolation='bilinear',
            vmin=0,
            vmax=1,
            origin='lower')

    def update(self, density_xz_tof_final):

        self.image_density_xz_tof_final.set_data(np.transpose(density_xz_tof_final))
