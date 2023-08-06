import numpy as np


class fig_density_xy_mask_tof_gpe(object):

    def __init__(self, ax, settings):

        ax.set_title('density (GPE)')

        ax.set_xlabel(r'$x$')
        ax.set_ylabel(r'$y$')

        ax.set_xlim([settings.x_min_tof_gpe, settings.x_max_tof_gpe])
        ax.set_ylim([settings.y_min_tof_gpe, settings.y_max_tof_gpe])

        ax.set_xticks([settings.x_min_tof_gpe, 0, settings.x_max_tof_gpe])
        ax.set_yticks([settings.y_min_tof_gpe, 0, settings.y_max_tof_gpe])

        density_xy_mask_tof_gpe = np.zeros((settings.Jx_tof_gpe, settings.Jy_tof_gpe))

        left = settings.x_min_tof_gpe
        right = settings.x_max_tof_gpe

        bottom = settings.y_min_tof_gpe
        top = settings.y_max_tof_gpe

        self.image_density_xy_mask_tof_gpe = ax.imshow(
            np.transpose(density_xy_mask_tof_gpe),
            extent=[left, right, bottom, top],
            cmap=settings.cmap_density_mask,
            aspect='auto',
            interpolation='bilinear',
            vmin=0,
            vmax=1,
            origin='lower')

    def update(self, density_xy_mask_tof_gpe):

        self.image_density_xy_mask_tof_gpe.set_data(np.transpose(density_xy_mask_tof_gpe))
