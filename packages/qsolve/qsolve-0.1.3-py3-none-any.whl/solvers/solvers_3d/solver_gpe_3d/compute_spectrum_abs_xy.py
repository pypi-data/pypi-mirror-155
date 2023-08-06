from qsolve.core import qsolve_core


def compute_spectrum_abs_xy(self, identifier, kwargs):

    if "rescaling" in kwargs:

        rescaling = kwargs["rescaling"]

    else:

        rescaling = False

    if identifier == "psi_tof_gpe":

        if "index_z" in kwargs:

            index_z = kwargs["index_z"]

        else:

            index_z = self.index_center_z_tof_free_gpe

        spectrum_abs_xy = qsolve_core.compute_spectrum_abs_xy_3d(self.psi_tof_free_gpe, index_z, rescaling)

    else:

        message = 'compute_spectrum_abs_xy(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)

    spectrum_abs_xy = spectrum_abs_xy.cpu().numpy()

    return spectrum_abs_xy
