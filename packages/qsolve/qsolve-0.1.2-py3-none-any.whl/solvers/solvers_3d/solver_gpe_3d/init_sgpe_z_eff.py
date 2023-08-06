from qsolve.core import qsolve_core


def init_sgpe_z_eff(self, kwargs):

    self.T_des_sgpe = kwargs["T_temp_des"] / self.units.unit_temperature
    self.mue_des_sgpe = kwargs["mue_des"] / self.units.unit_energy
    self.gamma_sgpe = kwargs["gamma"]
    self.dt_sgpe = kwargs["dt"] / self.units.unit_time

    z1 = kwargs["filter_z1"] / self.units.unit_length
    z2 = kwargs["filter_z2"] / self.units.unit_length

    s = kwargs["filter_z_s"] / self.units.unit_length

    self.filter_z_sgpe = qsolve_core.compute_filter_z_3d(self.z, z1, z2, s)
