def set_psi_0_tof_free_schroedinger(self, identifier, kwargs):

    if identifier == 'psi_tof_free_gpe':

        self.psi_0_tof_free_schroedinger = self.psi_tof_free_gpe

    else:

        message = 'set_psi_0_tof_free_schroedinger(identifier, **kwargs): ' \
                  'identifier \'{0:s}\' not supported'.format(identifier)

        raise Exception(message)
