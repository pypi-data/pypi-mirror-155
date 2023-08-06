from qsolve.utils.primes import get_prime_factors

import numpy as np

import torch


def init_time_of_flight(self, params):

    self.Jx_tof_free_gpe = params["Jx_tof_free_gpe"]
    self.Jy_tof_free_gpe = params["Jy_tof_free_gpe"]
    self.Jz_tof_free_gpe = params["Jz_tof_free_gpe"]

    self.T_tof_total = params["T_tof_total"] / self.units.unit_time
    self.T_tof_free_gpe = params["T_tof_free_gpe"] / self.units.unit_time

    self.T_tof_free_schroedinger = self.T_tof_total - self.T_tof_free_gpe

    self.dt_tof_free_gpe = self.dt

    self.dx_tof_free_gpe = self.dx
    self.dy_tof_free_gpe = self.dy
    self.dz_tof_free_gpe = self.dz

    # ---------------------------------------------------------------------------------------------
    self.n_time_steps_tof_free_gpe = int(np.round(self.T_tof_free_gpe / self.dt_tof_free_gpe))

    assert (self.n_time_steps_tof_free_gpe * self.dt_tof_free_gpe - self.T_tof_free_gpe) < 1e-14
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    assert (self.Jx_tof_free_gpe >= self.Jx)
    assert (self.Jy_tof_free_gpe >= self.Jy)
    assert (self.Jz_tof_free_gpe >= self.Jz)

    assert (self.Jx_tof_free_gpe % 2 == 0)
    assert (self.Jy_tof_free_gpe % 2 == 0)
    assert (self.Jz_tof_free_gpe % 2 == 0)

    prime_factors_Jx_tof_free_gpe = get_prime_factors(self.Jx_tof_free_gpe)
    prime_factors_Jy_tof_free_gpe = get_prime_factors(self.Jy_tof_free_gpe)
    prime_factors_Jz_tof_free_gpe = get_prime_factors(self.Jz_tof_free_gpe)

    assert (np.max(prime_factors_Jx_tof_free_gpe) < 11)
    assert (np.max(prime_factors_Jy_tof_free_gpe) < 11)
    assert (np.max(prime_factors_Jz_tof_free_gpe) < 11)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    x_tof_free_gpe = self.dx_tof_free_gpe * np.arange(-self.Jx_tof_free_gpe // 2, self.Jx_tof_free_gpe // 2)
    y_tof_free_gpe = self.dy_tof_free_gpe * np.arange(-self.Jy_tof_free_gpe // 2, self.Jy_tof_free_gpe // 2)
    z_tof_free_gpe = self.dz_tof_free_gpe * np.arange(-self.Jz_tof_free_gpe // 2, self.Jz_tof_free_gpe // 2)

    self.index_center_x_tof_free_gpe = np.argmin(np.abs(x_tof_free_gpe))
    self.index_center_y_tof_free_gpe = np.argmin(np.abs(y_tof_free_gpe))
    self.index_center_z_tof_free_gpe = np.argmin(np.abs(z_tof_free_gpe))

    assert (np.abs(x_tof_free_gpe[self.index_center_x_tof_free_gpe]) < 1e-14)
    assert (np.abs(y_tof_free_gpe[self.index_center_y_tof_free_gpe]) < 1e-14)
    assert (np.abs(z_tof_free_gpe[self.index_center_z_tof_free_gpe]) < 1e-14)

    self.x_tof_free_gpe = torch.tensor(x_tof_free_gpe, dtype=torch.float64, device=self.device)
    self.y_tof_free_gpe = torch.tensor(y_tof_free_gpe, dtype=torch.float64, device=self.device)
    self.z_tof_free_gpe = torch.tensor(z_tof_free_gpe, dtype=torch.float64, device=self.device)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    self.x_0_tof_free_schroedinger = self.x_tof_free_gpe
    self.y_0_tof_free_schroedinger = self.y_tof_free_gpe
    self.z_0_tof_free_schroedinger = self.z_tof_free_gpe

    Jx_tof_final = params["Jx_tof_final"]
    Jy_tof_final = params["Jy_tof_final"]
    Jz_tof_final = params["Jz_tof_final"]

    x_min_tof_final = params["x_min_tof_final"] / self.units.unit_length
    x_max_tof_final = params["x_max_tof_final"] / self.units.unit_length

    y_min_tof_final = params["y_min_tof_final"] / self.units.unit_length
    y_max_tof_final = params["y_max_tof_final"] / self.units.unit_length

    z_min_tof_final = params["z_min_tof_final"] / self.units.unit_length
    z_max_tof_final = params["z_max_tof_final"] / self.units.unit_length

    x_f_tof_free_schroedinger = np.linspace(x_min_tof_final, x_max_tof_final, Jx_tof_final, endpoint=True)
    y_f_tof_free_schroedinger = np.linspace(y_min_tof_final, y_max_tof_final, Jy_tof_final, endpoint=True)
    z_f_tof_free_schroedinger = np.linspace(z_min_tof_final, z_max_tof_final, Jz_tof_final, endpoint=True)

    index_center_x_f_tof_free_schroedinger = np.argmin(np.abs(x_f_tof_free_schroedinger))
    index_center_y_f_tof_free_schroedinger = np.argmin(np.abs(y_f_tof_free_schroedinger))
    index_center_z_f_tof_free_schroedinger = np.argmin(np.abs(z_f_tof_free_schroedinger))

    assert (np.abs(x_f_tof_free_schroedinger[index_center_x_f_tof_free_schroedinger]) < 5e-14)
    assert (np.abs(y_f_tof_free_schroedinger[index_center_y_f_tof_free_schroedinger]) < 5e-14)
    assert (np.abs(z_f_tof_free_schroedinger[index_center_z_f_tof_free_schroedinger]) < 5e-14)

    self.x_f_tof_free_schroedinger = torch.tensor(x_f_tof_free_schroedinger, dtype=torch.float64, device=self.device)
    self.y_f_tof_free_schroedinger = torch.tensor(y_f_tof_free_schroedinger, dtype=torch.float64, device=self.device)
    self.z_f_tof_free_schroedinger = torch.tensor(z_f_tof_free_schroedinger, dtype=torch.float64, device=self.device)

    self.index_center_x_f_tof_free_schroedinger = index_center_x_f_tof_free_schroedinger
    self.index_center_y_f_tof_free_schroedinger = index_center_y_f_tof_free_schroedinger
    self.index_center_z_f_tof_free_schroedinger = index_center_z_f_tof_free_schroedinger
    # ---------------------------------------------------------------------------------------------
