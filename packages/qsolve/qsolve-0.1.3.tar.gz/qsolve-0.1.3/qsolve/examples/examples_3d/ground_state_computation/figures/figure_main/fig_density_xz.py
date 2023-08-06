import numpy as np


class fig_density_xz(object):

    def __init__(self, ax, settings):

        ax.set_title("density", fontsize=settings.fontsize_titles)
    
        Jx = settings.Jx
        Jz = settings.Jz

        ax.set_xlabel(settings.label_z)
        ax.set_ylabel(settings.label_x)
        
        ax.set_xticks(settings.z_ticks)
        ax.set_yticks(settings.x_ticks)

        density_xz = np.zeros((Jx, Jz))

        left = settings.z_min
        right = settings.z_max

        bottom = settings.x_min
        top = settings.x_max

        self.image_density_xz = ax.imshow(density_xz,
                                          extent=[left, right, bottom, top],
                                          cmap=settings.cmap_density,
                                          aspect='auto',
                                          interpolation='bilinear',
                                          vmin=0,
                                          vmax=1,
                                          origin='lower')

    def update(self, density_xz):

        self.image_density_xz.set_data(density_xz)
