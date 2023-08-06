import numpy as np


class fig_real_part_xz(object):

    def __init__(self, ax, settings):

        ax.set_xlabel(settings.xlabel_xz)
        ax.set_ylabel(settings.ylabel_xz)

        ax.set_xticks(settings.z_ticks)
        ax.set_yticks(settings.x_ticks)

        real_part_xz = np.zeros((settings.Jx, settings.Jz))

        self.image_real_part_xz = ax.imshow(real_part_xz,
                                            extent=[settings.z_min, settings.z_max, settings.x_min, settings.x_max],
                                            cmap='RdBu',
                                            aspect='auto',
                                            interpolation='bilinear',
                                            vmin=-1,
                                            vmax=+1,
                                            origin='lower')

    def update(self, real_part_xz):

        self.image_real_part_xz.set_data(real_part_xz)
