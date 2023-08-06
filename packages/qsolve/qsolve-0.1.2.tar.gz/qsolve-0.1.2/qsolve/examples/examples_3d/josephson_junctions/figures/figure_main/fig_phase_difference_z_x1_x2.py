import numpy as np

from .. style import colors


class fig_phase_difference_z_x1_x2(object):

    def __init__(self, ax, settings):

        z = settings.z

        indices_z_restr = settings.indices_z_restr

        z_restr = z[indices_z_restr]

        self.line_phase_difference_z, = ax.plot(z_restr, np.zeros_like(z_restr), linewidth=1.00, linestyle='-', color=colors.wet_asphalt, label=r'single run')

        self.indices_z_restr = indices_z_restr

        ax.set_xlabel(settings.label_z)
        ax.set_ylabel(r'$\Delta \, \phi\; / \; \pi$')

        ax.set_xticks(settings.z_ticks)

        ax.set_yticks([-0.5, 0, 0.5], minor=False)
        ax.set_yticks([-0.75, -0.25, 0.25, 0.75], minor=True)

        ax.set_xlim(settings.z_min, settings.z_max)
        ax.set_ylim(-0.8, 0.8)

        ax.grid(visible=True, which='major', color=colors.color_gridlines_major, linestyle='-', linewidth=0.5)
        ax.grid(visible=True, which='minor', color=colors.color_gridlines_minor, linestyle='-', linewidth=0.5, alpha=0.2)

    def update(self, phase_difference_z):

        indices_z_restr = self.indices_z_restr

        self.line_phase_difference_z.set_ydata(phase_difference_z[indices_z_restr]/np.pi)
