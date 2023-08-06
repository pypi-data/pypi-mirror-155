import numpy as np

from numpy import zeros_like

from numpy import pi

from ..style import colors


class fig_phase_z(object):

    def __init__(self, ax, settings_graphics):

        self.hbar = settings_graphics.hbar

        self.m_atom = settings_graphics.m_atom

        self.line_phase_z, = ax.plot(settings_graphics.z, zeros_like(settings_graphics.z), linewidth=1, linestyle='-', color=colors.wet_asphalt)

        ax.set_xlim(settings_graphics.z_min, settings_graphics.z_max)
        
        ax.set_ylim(-1.2, 1.2)

        ax.set_xlabel(settings_graphics.xlabel_density_z)
        
        ax.set_xticks(settings_graphics.z_ticks)
        
        ax.grid(b=True, which='major', color=settings_graphics.color_gridlines_major, linestyle='-', linewidth=0.5)
        
        ax.set_ylabel(r'$\cos(\varphi)$')

        # -----------------------------------------------------------------------------------------
        ax_V_z = ax.twinx()
    
        self.line_V_z, = ax_V_z.plot(settings_graphics.z, zeros_like(settings_graphics.z), linewidth=1, linestyle='-', color=colors.sun_flower)

        ax_V_z.set_xlim(settings_graphics.z_min, settings_graphics.z_max)
        ax_V_z.set_ylim(settings_graphics.potential_min, settings_graphics.potential_max)
        
        ax_V_z.set_ylabel(settings_graphics.ylabel_V_x_y_z)
        # -----------------------------------------------------------------------------------------

    def update(self, phase_z, V_z):
        
        scaling_V = (self.hbar * 2 * pi * 1000)
        
        V_z = V_z / scaling_V
        
        self.line_phase_z.set_ydata(np.cos(phase_z))

        self.line_V_z.set_ydata(V_z)
