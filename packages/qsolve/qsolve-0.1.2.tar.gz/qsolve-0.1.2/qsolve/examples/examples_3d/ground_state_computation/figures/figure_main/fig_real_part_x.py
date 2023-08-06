from numpy import zeros_like

import numpy as np

from .. style import colors


class fig_real_part_x(object):

    def __init__(self, ax, settings):

        self.hbar = settings.hbar
        self.m_atom = settings.m_atom
    
        self.line_real_part_x, = ax.plot(settings.x, zeros_like(settings.x), linewidth=1, linestyle='-', color=colors.wet_asphalt)
        self.line_imag_part_x, = ax.plot(settings.x, zeros_like(settings.x), linewidth=1, linestyle='-', color=colors.peter_river)

        ax.set_ylim(settings.real_part_min, settings.real_part_max)
        
        ax.set_xlabel(settings.label_x)
        
        ax.grid(visible=True, which='major', color=settings.color_gridlines_major, linestyle='-', linewidth=0.5)
        
        ax.set_xticks(settings.x_ticks)
        
        ax.grid(visible=True, which='minor', color=settings.color_gridlines_minor, linestyle='-', linewidth=0.5, alpha=0.2)

        ax.set_ylabel(r'arbitrary units')

        # -----------------------------------------------------------------------------------------
        ax_V_x = ax.twinx()
    
        self.line_V_x, = ax_V_x.plot(settings.x, zeros_like(settings.x), linewidth=1, linestyle='-', color=colors.sun_flower)

        ax_V_x.set_xlim(settings.x_min, settings.x_max)
        ax_V_x.set_ylim(settings.V_min, settings.V_max)
        
        ax_V_x.set_ylabel(settings.label_V)
        # -----------------------------------------------------------------------------------------

    def update(self, real_part_x, imag_part_x, V_x):
        
        scaling_V = self.hbar * 2 * np.pi * 1000
        
        V_x = V_x / scaling_V

        self.line_real_part_x.set_ydata(real_part_x)
        self.line_imag_part_x.set_ydata(imag_part_x)
        
        self.line_V_x.set_ydata(V_x)
