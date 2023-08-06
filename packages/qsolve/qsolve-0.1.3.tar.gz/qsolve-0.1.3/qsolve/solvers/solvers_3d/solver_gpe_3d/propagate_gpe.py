from qsolve.core import qsolve_core


def propagate_gpe(self, kwargs):

    n_start = kwargs["n_start"]
    n_inc = kwargs["n_inc"]

    mue_shift = kwargs["mue_shift"] / self.units.unit_energy

    n_local = 0

    while n_local < n_inc:

        n = n_start + n_local

        if self.u_of_times.ndim > 1:

            u = 0.5 * (self.u_of_times[:, n] + self.u_of_times[:, n+1])

        else:

            u = 0.5 * (self.u_of_times[n] + self.u_of_times[n+1])

        self.V = self.potential.eval(u)

        self.psi = qsolve_core.propagate_gpe_3d(
            self.psi,
            self.V,
            self.dx,
            self.dy,
            self.dz,
            self.dt,
            mue_shift,
            self.hbar,
            self.m_atom,
            self.g)

        n_local = n_local + 1
