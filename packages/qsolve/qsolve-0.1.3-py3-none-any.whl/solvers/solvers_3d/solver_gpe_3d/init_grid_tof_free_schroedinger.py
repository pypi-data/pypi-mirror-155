import numpy as np

import torch


def init_grid_tof_free_schroedinger(self, kwargs):

    x_0_tof_free_schroedinger = kwargs["x_0"] / self.units.unit_length
    y_0_tof_free_schroedinger = kwargs["y_0"] / self.units.unit_length
    z_0_tof_free_schroedinger = kwargs["z_0"] / self.units.unit_length

    x_f_tof_free_schroedinger = kwargs["x_f"] / self.units.unit_length
    y_f_tof_free_schroedinger = kwargs["y_f"] / self.units.unit_length
    z_f_tof_free_schroedinger = kwargs["z_f"] / self.units.unit_length

    index_center_x_f_tof_free_schroedinger = np.argmin(np.abs(x_f_tof_free_schroedinger))
    index_center_y_f_tof_free_schroedinger = np.argmin(np.abs(y_f_tof_free_schroedinger))
    index_center_z_f_tof_free_schroedinger = np.argmin(np.abs(z_f_tof_free_schroedinger))

    assert (np.abs(x_f_tof_free_schroedinger[index_center_x_f_tof_free_schroedinger]) < 5e-14)
    assert (np.abs(y_f_tof_free_schroedinger[index_center_y_f_tof_free_schroedinger]) < 5e-14)
    assert (np.abs(z_f_tof_free_schroedinger[index_center_z_f_tof_free_schroedinger]) < 5e-14)

    self.x_0_tof_free_schroedinger = torch.tensor(x_0_tof_free_schroedinger, dtype=torch.float64, device=self.device)
    self.y_0_tof_free_schroedinger = torch.tensor(y_0_tof_free_schroedinger, dtype=torch.float64, device=self.device)
    self.z_0_tof_free_schroedinger = torch.tensor(z_0_tof_free_schroedinger, dtype=torch.float64, device=self.device)

    self.x_f_tof_free_schroedinger = torch.tensor(x_f_tof_free_schroedinger, dtype=torch.float64, device=self.device)
    self.y_f_tof_free_schroedinger = torch.tensor(y_f_tof_free_schroedinger, dtype=torch.float64, device=self.device)
    self.z_f_tof_free_schroedinger = torch.tensor(z_f_tof_free_schroedinger, dtype=torch.float64, device=self.device)

    self.index_center_x_f_tof_free_schroedinger = index_center_x_f_tof_free_schroedinger
    self.index_center_y_f_tof_free_schroedinger = index_center_y_f_tof_free_schroedinger
    self.index_center_z_f_tof_free_schroedinger = index_center_z_f_tof_free_schroedinger
