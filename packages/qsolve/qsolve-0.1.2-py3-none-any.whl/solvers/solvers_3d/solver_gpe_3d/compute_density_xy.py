from qsolve.core import qsolve_core


def compute_density_xy(self, identifier, kwargs):

    if "rescaling" in kwargs:

        rescaling = kwargs["rescaling"]

    else:

        rescaling = False

    if identifier == "psi_tof_gpe":

        if "index_z" in kwargs:

            index_z = kwargs["index_z"]

        else:

            index_z = self.index_center_z_tof_free_gpe

        density_xy = qsolve_core.compute_density_xy_3d(self.psi_tof_free_gpe, index_z, rescaling)

    elif identifier == "psi_f_tof_free_schroedinger":

        if "index_z" in kwargs:

            index_z = kwargs["index_z"]

        else:

            index_z = self.index_center_z_f_tof_free_schroedinger

        density_xy = qsolve_core.compute_density_xy_3d(self.psi_f_tof_free_schroedinger, index_z, rescaling)

    else:

        message = 'compute_density_xz(identifier, **kwargs): identifier \'{0:s}\' not supported'.format(identifier)

        raise Exception(message)

    return density_xy.cpu().numpy()
