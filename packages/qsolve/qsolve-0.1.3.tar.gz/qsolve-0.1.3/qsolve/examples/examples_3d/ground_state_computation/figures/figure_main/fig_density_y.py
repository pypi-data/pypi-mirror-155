from numpy import zeros_like

from numpy import pi

from .. style import colors


class fig_density_y(object):

    def __init__(self, ax, settings):

        self.hbar = settings.hbar
        self.m_atom = settings.m_atom

        self.line_density_y, = ax.plot(settings.y, zeros_like(settings.y),
                                       linewidth=1, linestyle='-', color=colors.wet_asphalt)

        ax.set_xlim(settings.y_min, settings.y_max)
        
        ax.set_ylim(settings.density_min, settings.density_max)
        
        ax.set_xlabel(settings.label_y)
        
        ax.set_xticks(settings.y_ticks)
        
        ax.grid(b=True, which='major', color=settings.color_gridlines_major, linestyle='-', linewidth=0.5)
        
        ax.set_ylabel(settings.label_density)
        
        ax.set_anchor('W')

        # -----------------------------------------------------------------------------------------
        ax_V_y = ax.twinx()
        
        self.line_V_y, = ax_V_y.plot(settings.y, zeros_like(settings.y),
                                     linewidth=1, linestyle='-', color=colors.sun_flower)

        ax_V_y.set_xlim(settings.y_min, settings.y_max)
        ax_V_y.set_ylim(settings.V_min, settings.V_max)
        
        ax_V_y.set_ylabel(settings.label_V)
        # -----------------------------------------------------------------------------------------

    def update(self, density_y, V_y):

        scaling_V = self.hbar * 2 * pi * 1000
        
        V_y = V_y / scaling_V

        self.line_density_y.set_ydata(density_y)

        self.line_V_y.set_ydata(V_y)
