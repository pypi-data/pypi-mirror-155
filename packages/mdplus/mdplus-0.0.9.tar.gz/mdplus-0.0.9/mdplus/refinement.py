# refinement.py - routines to improve geometry.
from mdplus import fast
import numpy as np
from scipy.optimize import minimize
from mdplus import utils


class ENM(object):

    def __init__(self, max_its=1000, tol=0.001, fc=0.1):
        """
        A Elastic Network-based Coordinate Optimiser.

        Adjusts the coordinates in each snapshot in a trajectory to
        optimise a set of distance restraints. The restraints may be
        provided explicitly or identified automatically from analysis
        of short distances in the structures in a training trajectory.

        The automatic method assumes the trajectory is of a single molecule
        and so, in graph-speak, is a single connected component.


        Args:
            max_its:    int, maximum number of refinement iterations.
            tol:        float, tolerance for termination
            fc:         float, force constant for elastic network

        Attributes:
            n_atoms:    int, number of atoms
            restraints: [n_restraints, 2] array of indices of restrained
                         atom pairs.
            d_ref:      [n_restraints] array of restrained distances.

        """
        self.max_its = max_its
        self.tol = tol
        self.fc = fc

        self.n_atoms = None
        self.restraints = None
        self.d_ref = None
        self.result = None

    def fit(self, X, restraints=None):
        """
        Train the refiner.

        If restraints is None, restraints are guessed from analysis of X.

        Args:
            X: [N_frames, N_atoms, 3] numpy array of coordinates.
            restraints: [N_bonds, 3] array of "bonded" atoms. Each row is
                        [i, j, r] where i and j are indices (cast to floats)
                        and r is the target distance.

        """
        X = utils.check_dimensions(X, ensure_traj=True)
        self.n_atoms = X.shape[1]
        if restraints is None:
            dm = utils.x2d(X)
            G = utils.make_graph(dm)
            restraints = utils.get_bonds(G)
            angles = utils.get_angles(G)
            ik = [[a[0], a[2]] for a in angles]
            restraints.extend(ik)
            self.restraints = np.array(restraints, dtype=np.int32)
            k = utils.pair_ind_to_dist_ind(self.n_atoms, self.restraints[:, 0],
                                           self.restraints[:, 1])
            self.d_ref = dm[k]
        else:
            self.restraints = np.array(restraints[:, :2], dtype=np.int32)
            self.d_ref = np.array(restraints[:, 2], dtype=np.float32)

    def get_state(self):
        """
        Get the state of the transformer as a dictionary

        """
        if self.n_atoms is None:
            raise RuntimeError("Error - the transformer has not been trained")
        config = {}
        for key in ['max_its', 'tol', 'fc', 'n_atoms']:
            config[key] = self.__dict__[key]
        config['restraints'] = self.restraints.tolist()
        config['d_ref'] = self.d_ref.tolist()
        config['result'] = None
        return config

    def set_state(self, config):
        """
        Set the state of the transformer from a dictionary

        """
        for key in ['max_its', 'tol', 'fc', 'n_atoms', 'result']:
            self.__dict__[key] = config[key]
        self.restraints = np.array(config['restraints'], dtype=np.int32)
        self.d_ref = np.array(config['d_ref'], dtype=np.float32)

    def transform(self, X):
        """
        Refine sets of coordinates.

        Args:
            X: [n_frames, n_atoms_3] or [n_atoms, 3] numpy array of coordinates

        Returns:
           [n_frames, n_atoms, 3] numpy array of refioned coordinates.
        """
        X = utils.check_dimensions(X)
        one_frame = len(X.shape) == 2
        if one_frame:
            X = X.reshape((1, -1, 3))
        if X.shape[1] != self.n_atoms:
            raise ValueError(f'Error: number of atoms in array'
                             f'to refine ({X.shape[1]})'
                             f' does not match number used to'
                             f' train refiner ({self.n_atoms})')
        Xout = []
        for Xc in X:
            self.result = minimize(fast.fg, Xc.flatten().astype(np.float32),
                                   method='TNC', jac=True,
                                   args=(self.restraints,
                                         self.d_ref.astype(np.float32),
                                         self.fc),
                                   options={'maxfun': self.max_its,
                                            'ftol': self.tol})
            Xout.append(self.result.x.reshape((-1, 3)))
        Xout = np.array(Xout)
        if one_frame:
            Xout = Xout[0]
        return Xout


def fix_bumps(X, dmin, dmax):
    """
    Fix bumps in coordinate array x using ENM approach.

    An elastic network is generated and optimised for X using all distances
    dij less than dmax. Target distances are set to max(dmin, dij)

    Args:
        X: [n_frames, n_atoms_3] or [n_atoms, 3] numpy array of coordinates
        dmin: float, threshold for what is a bump
        dmax: float, threshold for what is restrained

    Returns:
       [n_frames, n_atoms, 3] numpy array of refined coordinates.
    """
    X = utils.check_dimensions(X)
    one_frame = len(X.shape) == 2
    if one_frame:
        X = X.reshape((1, -1, 3))
    Xout = np.zeros_like(X)
    for iframe, Xc in enumerate(X):
        ij = utils.get_bumps(Xc, dmax)
        n_bumps = len(ij)
        rmin = np.zeros(n_bumps)
        for k in range(n_bumps):
            i, j = ij[k]
            dx = Xc[i] - Xc[j]
            r = np.sqrt((dx*dx).sum())
            rmin[k] = max(dmin, r)
        restraints = np.zeros((n_bumps, 3), dtype=np.float32)
        restraints[:, :2] = ij.astype(np.float32)
        restraints[:, 2] = rmin
        minimiser = ENM()
        minimiser.fit(Xc, restraints=restraints)
        Xout[iframe] = minimiser.transform(Xc)
    if one_frame:
        Xout = Xout[0]
    return Xout
