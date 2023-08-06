# utils.py
from mdplus.fast import rmsd_traj, fitted_traj, fitted_mean, bumps
import numpy as np
from scipy.spatial.distance import pdist
import networkx as nx


def compute_distances(xyz, bonds):
    bonds = np.array(bonds, dtype=np.int32)
    one_frame = len(xyz.shape) == 2
    if one_frame:
        xyz = xyz.reshape((1, -1, 3))
    xi = xyz[:, bonds[:, 0]]
    xj = xyz[:, bonds[:, 1]]
    dx = xi - xj
    dr = np.sqrt((dx * dx).sum(axis=2))
    if one_frame:
        dr = dr[0]
    return dr


def compute_angles(xyz, angles):
    angles = np.array(angles, dtype=np.int32)
    one_frame = len(xyz.shape) == 2
    if one_frame:
        xyz = xyz.reshape((1, -1,  3))
    xi = xyz[:, angles[:, 0]]
    xj = xyz[:, angles[:, 1]]
    xk = xyz[:, angles[:, 2]]
    v1 = xi - xj
    v2 = xk - xj
    v1 = v1 / np.linalg.norm(v1, axis=(2), keepdims=True)
    v2 = v2 / np.linalg.norm(v2, axis=(2), keepdims=True)
    d = (v1 * v2).sum(axis=2)
    a = np.arccos(d)
    if one_frame:
        a = a[0]
    return a


def compute_dihedrals(xyz, dihedrals):
    dihedrals = np.array(dihedrals, dtype=np.int32)
    one_frame = len(xyz.shape) == 2
    if one_frame:
        xyz = xyz.reshape((1, -1, 3))
    xi = xyz[:, dihedrals[:, 0]]
    xj = xyz[:, dihedrals[:, 1]]
    xk = xyz[:, dihedrals[:, 2]]
    xl = xyz[:, dihedrals[:, 3]]
    v1 = xj - xi
    v2 = xk - xj
    v3 = xl - xk
    c1 = np.cross(v2, v3)
    c2 = np.cross(v1, v2)

    p1 = (v1 * c1).sum(-1)
    p1 *= (v2 * v2).sum(-1) ** 0.5
    p2 = (c1 * c2).sum(-1)

    d = np.arctan2(p1, p2)
    if one_frame:
        d = d[0]
    return d


def get_bumps(x, dmin):
    """
    Find distances in x <= dmin

    Args:
        x: [n_atoms, 3] numpy array of coordinates
        dmin: float, minimum separation

    Returns:
        ij: [n_bumps, 2] integer array

    """
    x = np.array(x, dtype=np.float32)
    max_bumps = x.shape[0] * 6
    n_bumps = max_bumps
    while n_bumps >= max_bumps:
        max_bumps = int(max_bumps * 1.2)
        ij = np.zeros((max_bumps, 2), dtype=np.int32)
        n_bumps = bumps(x, ij, dmin)
    return ij[:n_bumps]


# Utility to get indices from condensed distance array
def dist_ind_to_pair_ind(d, i):
    b = 1 - 2 * d
    x = np.floor((-b - np.sqrt(b**2 - 8*i))/2).astype(int)
    y = (i + x * (b + x + 2) / 2 + 1).astype(int)
    return (x, y)


# Utility to get indices for condensed distance array
def pair_ind_to_dist_ind(d, i, j):
    index = d*(d-1)/2 - (d-i)*(d-i-1)/2 + j - i - 1
    return index.astype(int)


def x2d(traj, variance=False):
    """
    Generate mean distance array from trajectory x

    Optionally return variances as well.  Try to be reasonably
    memory-conservative.


    Args:
        traj: [n_atoms, 3] or [n_frames_n_atoms, 3] array
        variance: bool, if True, return variances as well.

    Returns:
        d: condensed mean distance matrix
        dvar: (optional): condensed distance variance matrix
    """
    traj = check_dimensions(traj, ensure_traj=True)
    s = None
    ss = None
    for x in traj:
        d = pdist(x)
        if s is None:
            s = d
            if variance:
                ss = d * d
        else:
            s += d
            if variance:
                ss += d * d
    n_frames = len(traj)
    d_mean = s / n_frames
    if variance:
        d_var = (ss / n_frames) - d_mean * d_mean
        return d_mean, d_var
    else:
        return d_mean


def make_graph(d, ring_sizes=[5, 6]):
    """
    Create a minimal connected graph from condensed distance matrix d
    """
    n_atoms = int(np.sqrt(len(d)*2)) + 1
    kl = np.argsort(d)
    il, jl = dist_ind_to_pair_ind(n_atoms, kl)
    G = nx.Graph()
    for i in range(n_atoms):
        G.add_node(i)
    dl = len(il)
    k = 0
    while k < dl and not nx.is_connected(G):
        i = il[k]
        j = jl[k]
        if not nx.has_path(G, i, j):
            G.add_edge(i, j, weight=d[kl[k]])
        elif len(nx.shortest_path(G, i, j)) in ring_sizes:
            G.add_edge(i, j, weight=d[kl[k]])
        k += 1
    return G


def get_bonds(G):
    """
    Extract bonds(edges) from graph G

    Args:
        G: Networkx Graph

    Returns:
        bonds: list of 2-element lists [i, j] where i and j are bonded.
    """
    return [e for e in G.edges]


# Utility function see:
#  https://stackoverflow.com/questions/28095646/finding-all-paths-walks-of-given-length-in-a-networkx-graph
def _findPaths(G, u, n):
    if n == 0:
        return [[u]]
    paths = [[u]+path for neighbor in G.neighbors(u)
             for path in _findPaths(G, neighbor, n-1) if u not in path]
    return paths


def get_angles(G):
    """
    Extract all unique angles from graph G
    Args:
        G: Networkx Graph

    Returns:
        angles: list of 3-element lists [i, j, k] where i < k.
    """
    all_paths = []
    for node in G:
        all_paths.extend(_findPaths(G, node, 2))
    unique_paths = []
    for p in all_paths:
        if p[0] < p[2]:
            unique_paths.append(p)
    return unique_paths


def rmsd(traj, xref):
    """
    Calculate rmsd between coordinates in traj and xref)

    Args:
        traj: [n_atoms, 3] or [n_frames_n_atoms, 3] array
        xref: [n_atoms, 3] or [n_frames_n_atoms, 3] array

    Returns:
        float or vector or array depending on dhapes of traj and xref
    """
    traj = check_dimensions(traj)
    one_frame = len(traj.shape) == 2
    if one_frame:
        traj = traj.reshape((1, -1, 3))
    xref = check_dimensions(xref)
    one_ref = len(xref.shape) == 2
    if one_ref:
        xref = xref.reshape((1, -1, 3))
    rmsd = np.zeros((len(traj), len(xref)))
    for i, r in enumerate(xref):
        rmsd[:, i] = rmsd_traj(traj, r)
    if one_ref:
        rmsd = rmsd.flatten()
    if one_ref and one_frame:
        rmsd = rmsd[0]
    return rmsd


def fit(traj, xref):
    """
    Least squares fit a trajectory to a reference structure

    Args:
        traj: [n_atoms, 3] or [n_frames_n_atoms, 3] array
        xref: [n_atoms, 3] or [n_frames_n_atoms, 3] array. if the latter,
              the first coordinate set is used for the fit.

    Returns:
        [n_frames, n_atoms, 3] array of fitted coordinates.f
    """
    traj = check_dimensions(traj)
    one_frame = len(traj.shape) == 2
    if one_frame:
        traj = traj.reshape((1, -1, 3))
    xref = check_dimensions(xref, ensure_traj=True)[0]

    fitted = fitted_traj(traj, xref)
    if one_frame:
        fitted = fitted[0]
    return fitted


def check_dimensions(traj, ensure_traj=False):
    """
    Check and regularize a trajectory array
    """
    traj = np.asarray(traj)
    if len(traj.shape) < 2 or len(traj.shape) > 3 or traj.shape[-1] != 3:
        raise ValueError('Error: traj must be an [n_atoms, 3]'
                         ' or [n_frames, n_atoms, 3] array')
    if len(traj.shape) == 2 and ensure_traj:
        traj = traj.reshape((1, -1, 3))
    return traj.astype(np.float32)


class Procrustes(object):

    def __init__(self, max_its=10, drmsd=0.01):
        """
        Initialise a procrustes least-squares fitter.

        Args:
            max_its: int, maximum number of iterations
            drmsd: float, target rmsd between successive means for convergence
        """
        self.max_its = max_its
        self.drmsd = drmsd
        self.mean = None

    def fit(self, X):
        """
        Train the fitter.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        """
        X = check_dimensions(X, ensure_traj=True)
        old_mean = X[0].copy()
        err = self.drmsd + 1.0
        it = 0
        while err > self.drmsd and it < self.max_its:
            it += 1
            new_mean = fitted_mean(X, old_mean)
            err = rmsd(old_mean, new_mean)
            old_mean = new_mean

        self.converged = err <= self.drmsd
        self.mean = old_mean

    def get_state(self):
        """
        Get current state of the fitter

        """
        if self.mean is None:
            return RuntimeError('Error: fitter has not been trained')
        config = {}
        config['mean'] = self.mean.tolist()
        config['max_its'] = self.max_its
        config['drmsd'] = self.drmsd
        config['converged'] = bool(self.converged)
        return config

    def set_state(self, config):
        """
        Set the state of the fitter

        """
        self.mean = np.array(config['mean'], dtype=np.float32)
        self.max_its = config['max_its']
        self.drmsd = config['drmsd']
        self.converged = config['converged']

    def transform(self, X):
        """
        Least-squares fit the coordinates in X.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        Returns:
            [n_frames, n_atoms, 3] numpy array of fitted coordinates
        """
        X = check_dimensions(X)
        one_frame = len(X.shape) == 2
        if one_frame:
            X = X.reshape((1, -1, 3))
        Xf = fit(X, self.mean)
        if one_frame:
            Xf = Xf[0]
        return Xf

    def fit_transform(self, X):
        """
        Train the fitter, and apply to X.

        Args:
            X: [n_frames, n_atoms, 3] numpy array
        Returns:
            [n_frames, n_atoms, 3] numpy array of fitted coordinates
        """
        self.fit(X)
        return self.transform(X)
