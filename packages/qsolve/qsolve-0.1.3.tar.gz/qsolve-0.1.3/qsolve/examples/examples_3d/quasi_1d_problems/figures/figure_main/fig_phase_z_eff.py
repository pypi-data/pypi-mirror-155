import numpy as np

from numpy import zeros_like

from numpy import pi

from .. style import colors


class fig_phase_z_eff(object):

    def __init__(self, ax, settings):

        self.hbar = settings.hbar

        self.m_atom = settings.m_atom

        self.line_phase_z_eff, = ax.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='-', color=colors.wet_asphalt, label='effective')
        self.line_phase_z, = ax.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='--', color=colors.peter_river, label='$x=y=0$')

        ax.set_xlim(settings.z_min, settings.z_max)
        ax.set_ylim(-1.2, 1.2)

        ax.set_xlabel(settings.label_z)
        
        ax.set_xticks(settings.z_ticks)
        
        ax.grid(visible=True, which='major', color=settings.color_gridlines_major, linestyle='-', linewidth=0.5)

        ax.set_ylabel(r'$\cos(\varphi)$')

        ax.legend(loc='lower right', bbox_to_anchor=(1.0, 0.0),
                  fancybox=settings.fancybox, framealpha=settings.framealpha, ncol=1)

        # -----------------------------------------------------------------------------------------
        ax_V_z = ax.twinx()
    
        self.line_V_z, = ax_V_z.plot(settings.z, zeros_like(settings.z),
                                     linewidth=1, linestyle='-', color=colors.sun_flower)

        ax_V_z.set_xlim(settings.z_min, settings.z_max)
        ax_V_z.set_ylim(settings.V_min, settings.V_max)
        
        ax_V_z.set_ylabel(settings.label_V)
        # -----------------------------------------------------------------------------------------

    def update(self, phase_z_eff, phase_z, V_z):

        scaling_V = self.hbar * 2 * pi * 1000
        
        V_z = V_z / scaling_V

        self.line_phase_z_eff.set_ydata(np.cos(phase_z_eff))
        self.line_phase_z.set_ydata(np.cos(phase_z))

        self.line_V_z.set_ydata(V_z)
