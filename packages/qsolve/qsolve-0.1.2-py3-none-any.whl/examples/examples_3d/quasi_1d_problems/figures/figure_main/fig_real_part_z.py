from numpy import zeros_like

from numpy import pi

from .. style import colors


class fig_real_part_z(object):

    def __init__(self, ax, settings):

        self.hbar = settings.hbar

        self.m_atom = settings.m_atom

        self.line_real_part_z, = ax.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='-', color=colors.wet_asphalt, label=r'$\Re\, \psi$')
        self.line_imag_part_z, = ax.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='-', color=colors.peter_river, label=r'$\Im\, \psi$')

        ax.set_xlim(settings.z_min, settings.z_max)

        ax.set_ylim(settings.real_part_min, settings.real_part_max)

        ax.set_xlabel(settings.label_z)
        
        ax.set_xticks(settings.z_ticks)
        
        ax.grid(b=True, which='major', color=settings.color_gridlines_major, linestyle='-', linewidth=0.5)

        ax.set_ylabel(r'arbitrary units')

        ax.legend(loc='lower right', bbox_to_anchor=(1.0, 0.0), fancybox=settings.fancybox, framealpha=settings.framealpha, ncol=1)
        
        # -----------------------------------------------------------------------------------------
        ax_V_z = ax.twinx()
    
        self.line_V_z, = ax_V_z.plot(settings.z, zeros_like(settings.z), linewidth=1, linestyle='-', color=colors.sun_flower)

        ax_V_z.set_xlim(settings.z_min, settings.z_max)
        ax_V_z.set_ylim(settings.V_min, settings.V_max)
        
        ax_V_z.set_ylabel(settings.label_V)
        # -----------------------------------------------------------------------------------------

    def update(self, real_part_z, imag_part_z, V_z):
        
        scaling_V = self.hbar * 2 * pi * 1000
        
        V_z = V_z / scaling_V
        
        self.line_real_part_z.set_ydata(real_part_z)
        self.line_imag_part_z.set_ydata(imag_part_z)

        self.line_V_z.set_ydata(V_z)
