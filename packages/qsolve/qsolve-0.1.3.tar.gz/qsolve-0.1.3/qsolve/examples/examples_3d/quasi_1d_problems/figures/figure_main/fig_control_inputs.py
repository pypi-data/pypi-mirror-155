import numpy as np

from .. style import colors


class fig_control_inputs(object):

    def __init__(self, ax, settings):
        
        self.line_u1_of_times, = ax.plot(settings.times,
                                         np.zeros_like(settings.times),
                                         linewidth=1, linestyle='-', color=colors.wet_asphalt,
                                         label=r'$u_1$')

        # self.line_u2_of_times, = ax.plot(settings.times,
        #                                  np.zeros_like(settings.times),
        #                                  linewidth=1, linestyle='--', color=colors.wet_asphalt,
        #                                  label=r'$u_2$')

        # self.line_u3_of_times, = ax.plot(settings.times,
        #                                  np.zeros_like(settings.times),
        #                                  linewidth=1, linestyle='-', color=colors.wet_asphalt,
        #                                  label=r'$u_3$')
        
        self.line_t_indicator, = ax.plot([0, 0], [-0.25, 1.25], linewidth=1, linestyle='--', color=colors.wet_asphalt)

        ax.set_xlim(settings.t_min, settings.t_max)
        
        ax.set_ylim(-0.1, 1.1)
        
        ax.set_xticks(settings.t_ticks_major, minor=False)
        ax.set_xticks(settings.t_ticks_minor, minor=True)
        
        ax.set_yticks([0, 0.5, 1], minor=False)
        ax.set_yticks([0.25, 0.75], minor=True)
        
        ax.grid(visible=True, which='major', color=colors.color_gridlines_major, linestyle='-', linewidth=0.5)
        ax.grid(visible=True, which='minor', color=colors.color_gridlines_minor, linestyle='-', linewidth=0.5,
                alpha=0.2)

        ax.set_xlabel(settings.label_t)
        ax.set_ylabel(r'control inputs')
        
        # ax.legend(loc='lower right',
        # bbox_to_anchor=(1.0, 0.05), ncol=1, framealpha=settings.framealpha, fancybox=settings.fancybox)

    def update_u(self, u1_of_times):

        self.line_u1_of_times.set_ydata(u1_of_times)
        # self.line_u2_of_times.set_ydata(u_of_times[1, :])
        # self.line_u3_of_times.set_ydata(u_of_times[2, :])

    def update_t(self, t):
        
        self.line_t_indicator.set_xdata([t/1e-3, t/1e-3])
