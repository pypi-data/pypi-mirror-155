from qsolve.utils.primes import get_prime_factors

import numpy as np

import torch


def init_grid_tof_free_gpe(self, kwargs):

    self.Jx_tof_free_gpe = kwargs["Jx"]
    self.Jy_tof_free_gpe = kwargs["Jy"]
    self.Jz_tof_free_gpe = kwargs["Jz"]

    self.dt_tof_free_gpe = kwargs["dt"] / self.units.unit_time

    self.dx_tof_free_gpe = self.dx
    self.dy_tof_free_gpe = self.dy
    self.dz_tof_free_gpe = self.dz

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
