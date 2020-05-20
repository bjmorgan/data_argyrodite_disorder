import numpy as np

def displacements_from_structures(structures):
    """Calculate cumulative atomic displacements from a sequence of pymatgen Structure objects.

    Args:
        structures ([Structure]): list of Structure objects (these must be time-ordered).

    Returns:
        (np.array):  Numpy array of cumulative displacements, 
            with shape [atom, timestep, axis]

    """
    points = [np.array(s.frac_coords)[:, np.newaxis] for s in structures]
    lattices = [s.lattice.matrix for s in structures]
    points.insert(0, points[0])
    lattices.insert(0, lattices[0]) 
    points = np.concatenate(points, axis=1)
    dp = points[:, 1:] - points[:, :-1]
    dp = dp - np.round(dp) # minimum-image convention
    frac_disp = np.cumsum(dp, axis=1)
    cart_disp = []
    for i in frac_disp:
        cart_disp.append([np.dot(d, m) for d, m in zip(i, lattices[1:])])
    disp = np.array(cart_disp)
    return disp

class DiffusionAnalyzer(object):

    def __init__(self, structure, displacements, specie, temperature,
                 time_step, step_skip, smoothed="max", min_obs=30, 
                 avg_nsteps=1000, lattices=None):
        """Modified pymatgen DiffusionAnalyzer constructor

        """
        self.structure = structure
        self.disp = displacements
        self.specie = specie
        self.time_step = time_step
        self.step_skip = step_skip
        self.min_obs = min_obs
        self.smoothed = smoothed
        self.avg_nsteps = avg_nsteps
        self.lattices = lattices

        if lattices is None:
            self.lattices = np.array([structure.lattice.matrix.tolist()])

        indices = []
        framework_indices = []
        for i, site in enumerate(structure):
            if site.specie.symbol == specie:
                indices.append(i)
            else:
                framework_indices.append(i)
        if self.disp.shape[1] < 2:
            self.diffusivity = 0.
            self.conductivity = 0.
            self.diffusivity_components = np.array([0., 0., 0.])
            self.conductivity_components = np.array([0., 0., 0.])
            self.max_framework_displacement = 0
        else:
            framework_disp = self.disp[framework_indices]
            drift = np.average(framework_disp, axis=0)[None, :, :]

            # drift corrected position
            dc = self.disp - drift

            nions, nsteps, dim = dc.shape

            if not smoothed:
                timesteps = np.arange(0, nsteps)
            elif smoothed == "constant":
                if nsteps <= avg_nsteps:
                    raise ValueError('Not enough data to calculate diffusivity')
                timesteps = np.arange(0, nsteps - avg_nsteps)
            else:
                # limit the number of sampled timesteps to 200
                min_dt = int(1000 / (self.step_skip * self.time_step))
                max_dt = min(len(indices) * nsteps // self.min_obs, nsteps)
                if min_dt >= max_dt:
                    raise ValueError('Not enough data to calculate diffusivity')
                timesteps = np.arange(min_dt, max_dt,
                                      max(int((max_dt - min_dt) / 200), 1))

            dt = timesteps * self.time_step * self.step_skip

            # calculate the smoothed msd values
            msd = np.zeros_like(dt, dtype=np.double)
            sq_disp_ions = np.zeros((len(dc), len(dt)), dtype=np.double)
            sq_disp_store = []
            msd_components = np.zeros(dt.shape + (3,))

            # calculate mean square charge displacement
            mscd = np.zeros_like(msd, dtype=np.double)

            for i, n in enumerate(timesteps):
                if not smoothed:
                    dx = dc[:, i:i + 1, :]
                    dcomponents = dc[:, i:i + 1, :]
                elif smoothed == "constant":
                    dx = dc[:, i:i + avg_nsteps, :] - dc[:, 0:avg_nsteps, :]
                    dcomponents = dc[:, i:i + avg_nsteps, :] - dc[:, 0:avg_nsteps, :]
                else:
                    dx = dc[:, n:, :] - dc[:, :-n, :]
                    dcomponents = dc[:, n:, :] - dc[:, :-n, :]

                # Get msd
                sq_disp = dx ** 2
                sq_disp_store.append( np.sum(sq_disp, axis=2)[indices] )
                sq_disp_ions[:, i] = np.average(np.sum(sq_disp, axis=2), axis=1)
                msd[i] = np.average(sq_disp_ions[:, i][indices])
                msd_components[i] = np.average(dcomponents[indices] ** 2,
                                               axis=(0, 1))

                # Get mscd
                sq_chg_disp = np.sum(dx[indices, :, :], axis=0) ** 2
                mscd[i] = np.average(np.sum(sq_chg_disp, axis=1), axis=0) / len(indices)

            self.msd = msd
            self.mscd = mscd
            self.sq_disp_ions = sq_disp_ions
            self.sq_disp_store = sq_disp_store
            self.msd_components = msd_components
            self.dt = dt
            self.indices = indices
            self.framework_indices = framework_indices

