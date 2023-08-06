from qsolve.core import qsolve_core


def compute_density_xz(self, identifier, kwargs):

    if "rescaling" in kwargs:

        rescaling = kwargs["rescaling"]

    else:

        rescaling = False

    if identifier == "psi_tof_gpe":

        if "index_y" in kwargs:

            index_y = kwargs["index_y"]

        else:

            index_y = self.index_center_y_tof_free_gpe

        density_xz = qsolve_core.compute_density_xz_3d(self.psi_tof_free_gpe, index_y, rescaling)

    elif identifier == "psi_f_tof_free_schroedinger":

        if "index_y" in kwargs:

            index_y = kwargs["index_y"]

        else:

            index_y = self.index_center_y_f_tof_free_schroedinger

        density_xz = qsolve_core.compute_density_xz_3d(self.psi_f_tof_free_schroedinger, index_y, rescaling)

    else:

        message = 'compute_density_xz(identifier, **kwargs): identifier \'{0:s}\' not supported'.format(identifier)

        raise Exception(message)

    return density_xz.cpu().numpy()
