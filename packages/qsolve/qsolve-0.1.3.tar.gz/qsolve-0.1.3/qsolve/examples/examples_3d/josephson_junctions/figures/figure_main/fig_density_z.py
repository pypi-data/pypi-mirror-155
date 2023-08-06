from numpy import zeros_like

from numpy import pi

from .. style import colors


class fig_density_z(object):

    def __init__(self, ax, settings):

        self.hbar = settings.hbar

        self.m_atom = settings.m_atom

        self.line_density_z_x1, = ax.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='-',
                                          color=colors.peter_river, label=r'$|\psi(x_1, 0, z)|^2$')

        self.line_density_z_x2, = ax.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='-',
                                          color=colors.wet_asphalt, label=r'$|\psi(x_2, 0, z)|^2$')

        ax.set_xlim(settings.z_min, settings.z_max)
        
        ax.set_ylim(settings.density_min, settings.density_max)

        ax.set_xlabel(settings.label_z)
        
        ax.set_xticks(settings.z_ticks)
        
        ax.grid(visible=True, which='major', color=settings.color_gridlines_major, linestyle='-', linewidth=0.5)
        
        ax.set_ylabel(settings.label_density)

        ax_V_z_x1 = ax.twinx()

        self.line_V_z_x1, = ax_V_z_x1.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='-',
                                           color=colors.sun_flower, label=r'$V(x_1, 0, z)$')

        ax_V_z_x1.set_xlim(settings.z_min, settings.z_max)
        ax_V_z_x1.set_ylim(settings.V_min, settings.V_max)

        ax_V_z_x1.set_ylabel(settings.label_V)

        ax_V_z_x1.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), fancybox=False, framealpha=1.0, ncol=1)

    def update(self, density_z_x1, density_z_x2, V_z_x1):

        scaling_V = self.hbar * 2 * pi * 1000

        V_z_x1 = V_z_x1 / scaling_V

        self.line_density_z_x1.set_ydata(density_z_x1)
        self.line_density_z_x2.set_ydata(density_z_x2)

        self.line_V_z_x1.set_ydata(V_z_x1)
