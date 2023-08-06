import numpy as np


def eval_data(solver):

    dx = solver.get('dx')
    dy = solver.get('dy')
    dz = solver.get('dz')

    index_center_x = solver.get('index_center_x')
    index_center_y = solver.get('index_center_y')
    index_center_z = solver.get('index_center_z')

    data = type('', (), {})()

    # ---------------------------------------------------------------------------------------------
    V = solver.get('V')

    V_x = np.squeeze(V[:, index_center_y, index_center_z])
    V_y = np.squeeze(V[index_center_x, :, index_center_z])
    V_z = np.squeeze(V[index_center_x, index_center_y, :])

    V_xz = np.squeeze(V[:, index_center_y, :])
    V_xy = np.squeeze(V[:, :, index_center_z])

    data.V = V

    data.V_x = V_x
    data.V_y = V_y
    data.V_z = V_z

    data.V_xz = V_xz
    data.V_xy = V_xy
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    psi = solver.get('psi')

    psi_x = np.squeeze(psi[:, index_center_y, index_center_z])
    psi_y = np.squeeze(psi[index_center_x, :, index_center_z])
    psi_z = np.squeeze(psi[index_center_x, index_center_y, :])

    psi_xz = np.squeeze(psi[:, index_center_y, :])
    psi_xy = np.squeeze(psi[:, :, index_center_z])

    data.psi = psi

    data.psi_x = psi_x
    data.psi_y = psi_y
    data.psi_z = psi_z

    data.psi_xz = psi_xz
    data.psi_xy = psi_xy
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    phase = np.angle(psi)

    phase_x = np.squeeze(phase[:, index_center_y, index_center_z])
    phase_y = np.squeeze(phase[index_center_x, :, index_center_z])
    phase_z = np.squeeze(phase[index_center_x, index_center_y, :])

    phase_xz = np.squeeze(phase[:, index_center_y, :])
    phase_xy = np.squeeze(phase[:, :, index_center_z])

    tmp = dx * dy * np.sum(psi, (0, 1), keepdims=False)

    phase_z_eff = np.angle(tmp)

    data.phase_x = phase_x
    data.phase_y = phase_y
    data.phase_z = phase_z

    data.phase_xz = phase_xz
    data.phase_xy = phase_xy

    data.phase_z_eff = phase_z_eff
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    density = np.real(psi * np.conj(psi))

    density_max = np.max(density)

    density_x = np.abs(psi_x) ** 2
    density_y = np.abs(psi_y) ** 2
    density_z = np.abs(psi_z) ** 2

    density_xz = np.abs(psi_xz) ** 2
    density_xy = np.abs(psi_xy) ** 2

    if density_max > 0:

        density_xz = density_xz / density_max
        density_xy = density_xy / density_max

    density_x_eff = dy * dz * np.sum(density, (1, 2), keepdims=False)
    density_y_eff = dx * dz * np.sum(density, (0, 2), keepdims=False)
    density_z_eff = dx * dy * np.sum(density, (0, 1), keepdims=False)

    data.density = density

    data.density_x = density_x
    data.density_y = density_y
    data.density_z = density_z

    data.density_xz = density_xz
    data.density_xy = density_xy

    data.density_x_eff = density_x_eff
    data.density_y_eff = density_y_eff
    data.density_z_eff = density_z_eff
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    real_part = np.real(psi)

    real_part_x = np.real(psi_x)
    real_part_y = np.real(psi_y)
    real_part_z = np.real(psi_z)

    imag_part_x = np.imag(psi_x)
    imag_part_y = np.imag(psi_y)
    imag_part_z = np.imag(psi_z)

    real_part_xz = np.real(psi_xz)
    real_part_xy = np.real(psi_xy)

    data.real_part = real_part

    data.real_part_x = real_part_x
    data.real_part_y = real_part_y
    data.real_part_z = real_part_z

    data.imag_part_x = imag_part_x
    data.imag_part_y = imag_part_y
    data.imag_part_z = imag_part_z

    data.real_part_xz = real_part_xz
    data.real_part_xy = real_part_xy
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    data.N = solver.compute_n_atoms('psi')
    # ---------------------------------------------------------------------------------------------

    return data
