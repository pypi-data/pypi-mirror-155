from numpy import zeros_like

from numpy import pi

from .. style import colors


class fig_density_z_eff(object):

    def __init__(self, ax, settings):

        self.hbar = settings.hbar

        self.m_atom = settings.m_atom

        self.line_density_z_eff, = ax.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='-', color=colors.wet_asphalt)

        ax.set_xlim(settings.z_min, settings.z_max)

        ax.set_ylim(settings.density_z_eff_min, settings.density_z_eff_max)

        ax.set_xlabel(settings.label_z)
        
        ax.set_xticks(settings.z_ticks)
        
        ax.grid(visible=True, which='major', color=settings.color_gridlines_major, linestyle='-', linewidth=0.5)
        
        ax.set_ylabel(settings.label_density_effective)

        # -----------------------------------------------------------------------------------------
        ax_V_z = ax.twinx()
    
        self.line_V_z, = ax_V_z.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='-', color=colors.sun_flower)

        ax_V_z.set_xlim(settings.z_min, settings.z_max)
        ax_V_z.set_ylim(settings.V_min, settings.V_max)
        
        ax_V_z.set_ylabel(settings.label_V)
        # -----------------------------------------------------------------------------------------

    def update(self, density_z_eff, V_z):

        scaling_V = self.hbar * 2 * pi * 1000
        
        V_z = V_z / scaling_V
        
        self.line_density_z_eff.set_ydata(density_z_eff / 1e06)

        self.line_V_z.set_ydata(V_z)
