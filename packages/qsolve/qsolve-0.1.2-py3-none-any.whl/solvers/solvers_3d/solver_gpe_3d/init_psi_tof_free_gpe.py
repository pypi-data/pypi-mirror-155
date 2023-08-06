from qsolve.core import qsolve_core


def init_psi_tof_free_gpe(self, identifier, kwargs):

    if identifier == 'psi':

        self.psi_tof_free_gpe = qsolve_core.init_psi_tof_free_gpe(
            self.psi,
            self.Jx_tof_free_gpe,
            self.Jy_tof_free_gpe,
            self.Jz_tof_free_gpe)

    else:

        message = 'init_psi_tof_free_gpe(self, identifier, **kwargs): \'identifier \'{0:s}\' ' \
                  'not supported'.format(identifier)

        raise Exception(message)
