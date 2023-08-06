import numpy as np


class fig_phase_difference_xy(object):

    def __init__(self, ax, settings):

        Jx = settings.Jx
        Jy = settings.Jy

        ax.set_xlabel(settings.label_y)
        ax.set_ylabel(settings.label_x)

        ax.set_xticks(settings.y_ticks)
        ax.set_yticks(settings.x_ticks)

        psi_imag_xy = np.zeros((Jx, Jy))

        left = settings.y_min
        right = settings.y_max

        bottom = settings.x_min
        top = settings.x_max

        ax.set_anchor('W')

        self.image_phase_difference_xy = ax.imshow(psi_imag_xy,
            extent=[left, right, bottom, top],
            cmap=settings.cmap_phase,
            aspect='equal',
            interpolation='bilinear',
            vmin=-1,
            vmax=1,
            origin='lower')

    def update(self, phase_difference_xy):

        self.image_phase_difference_xy.set_data(phase_difference_xy)
