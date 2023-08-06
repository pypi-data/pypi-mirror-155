from numpy import zeros_like

import numpy as np

from .. style import colors


class fig_density_x(object):

    def __init__(self, ax, settings):

        self.hbar = settings.hbar
        self.m_atom = settings.m_atom
    
        self.line_density_x, = ax.plot(settings.x, zeros_like(settings.x),
                                       linewidth=1, linestyle='-', color=colors.wet_asphalt)

        ax.set_ylim(settings.density_min, settings.density_max)
        
        ax.set_xlabel(settings.label_x)
        
        ax.grid(visible=True, which='major', color=settings.color_gridlines_major, linestyle='-', linewidth=0.5)
        
        ax.set_xticks(settings.x_ticks)
        
        ax.grid(visible=True, which='minor', color=settings.color_gridlines_minor,
                linestyle='-', linewidth=0.5, alpha=0.2)
        
        ax.set_ylabel(settings.label_density)

        ax_V_x = ax.twinx()
    
        self.line_V_x, = ax_V_x.plot(
            settings.x, zeros_like(settings.x),
            linewidth=1, linestyle='-', color=colors.sun_flower)

        ax_V_x.set_xlim(settings.x_min, settings.x_max)
        ax_V_x.set_ylim(settings.V_min, settings.V_max)
        
        ax_V_x.set_ylabel(settings.label_V)

    def update(self, density_x, V_x):
        
        scaling_V = self.hbar * 2 * np.pi * 1000
        
        V_x = V_x / scaling_V

        self.line_density_x.set_ydata(density_x)
        
        self.line_V_x.set_ydata(V_x)
