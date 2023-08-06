from qsolve.core import qsolve_core


def compute_spectrum_abs_xz(self, identifier, kwargs):

    if "rescaling" in kwargs:

        rescaling = kwargs["rescaling"]

    else:

        rescaling = False

    if identifier == "psi_tof_gpe":

        if "index_y" in kwargs:

            index_y = kwargs["index_y"]

        else:

            index_y = self.index_center_y_tof_free_gpe

        spectrum_abs_xz = qsolve_core.compute_spectrum_abs_xz_3d(self.psi_tof_free_gpe, index_y, rescaling)

    else:

        message = 'compute_spectrum_abs_xy(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)

    spectrum_abs_xz = spectrum_abs_xz.cpu().numpy()

    return spectrum_abs_xz
