import numpy as np


class fig_phase_difference_xz(object):

    def __init__(self, ax, settings):

        ax.set_title("phase difference", fontsize=settings.fontsize_titles)

        Jx = settings.Jx
        Jz = settings.Jz

        ax.set_xlabel(settings.label_z)
        ax.set_ylabel(settings.label_x)

        ax.set_xticks(settings.z_ticks)
        ax.set_yticks(settings.x_ticks)

        phase_difference_xz = np.zeros((Jx, Jz))

        left = settings.z_min
        right = settings.z_max

        bottom = settings.x_min
        top = settings.x_max

        self.image_phase_difference_xz = ax.imshow(
            phase_difference_xz,
            extent=[left, right, bottom, top],
            cmap=settings.cmap_phase,
            aspect='auto',
            interpolation='bilinear',
            vmin=-1,
            vmax=1,
            origin='lower')

    def update(self, phase_difference_xz):

        self.image_phase_difference_xz.set_data(phase_difference_xz)
