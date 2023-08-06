import numpy as np
from mdplus.pca import PCA
from mdplus.refinement import ENM
from mdplus import utils
from mdplus.fast import rv
from sklearn.linear_model import LinearRegression
from scipy.spatial.distance import squareform, pdist, cdist

# Zmatrix utilities for Shave/Sprout adapted from
# https://github.com/tmpchem/computational_chemistry/blob/b44ee6d2e1d2ec203811140b732cdb38f5164d76/scripts/geometry_analysis/zmat2xyz.py


# calculate distance between two 3-d cartesian coordinates
def _get_r12(coords1, coords2):
    r = np.linalg.norm(coords1 - coords2)
    return r


# calculate unit vector between to 3-d cartesian coordinates
def _get_u12(coords1, coords2):
    r12 = _get_r12(coords1, coords2)
    u12 = (coords2 - coords1) / r12
    return u12


# calculate dot product between two unit vectors
def _get_udp(uvec1, uvec2):
    udp = np.dot(uvec1, uvec2)
    return udp


# calculate unit cross product between two unit vectors
def _get_ucp(uvec1, uvec2):
    ucp = np.cross(uvec1, uvec2)
    return ucp / np.linalg.norm(ucp)


# get local axis system from 3 coordinates
def _get_local_axes(coords1, coords2, coords3):
    u21 = _get_u12(coords1, coords2)
    u23 = _get_u12(coords2, coords3)
    if (abs(_get_udp(u21, u23)) >= 1.0):
        raise ValueError(
            'Error: Co-linear atoms in an '
            'internal coordinate definition'
            )
    u23c21 = _get_ucp(u23, u21)
    u21c23c21 = _get_ucp(u21, u23c21)
    z = u21
    y = u21c23c21
    x = _get_ucp(y, z)
    local_axes = [x, y, z]
    return local_axes


# calculate vector of bond in local axes of internal coordinates
def _get_bond_vector(r, a, t):
    x = r * np.sin(a) * np.sin(t)
    y = r * np.sin(a) * np.cos(t)
    z = r * np.cos(a)
    bond_vector = [x, y, z]
    return bond_vector

# Functions for shave and sprout:


def _make_tmat(x, d):
    """
    Make a T-matrix for x

    A T-matrix is a partial Z-matrix, just for terminal atoms
    Each row is: i, j, k, l, r, a, t
    where i, j, k, l are the Z-matrix indices (i is the terminal
    atom, j, k and l are non-terminal) and r, a, t are the bond
    length, angle and torsion. Indices i-l are cast to floats.
    """

    n_tot = len(x)
    G = utils.make_graph(d)
    terminii = [i for i in range(n_tot) if len(G[i]) == 1]
    d = squareform(d)
    d[:, terminii] = d.max() + 1.0
    Tind = np.zeros((len(terminii), 4), dtype=np.int32)
    Tind[:, 0] = terminii
    Tind[:, 1:] = np.argsort(d, axis=1)[terminii][:, :3]
    Tind = Tind[Tind[:, 1].argsort()]
    for i in range(1, len(Tind)):
        if Tind[i, 1] == Tind[i-1, 1]:
            Tind[i, 2:] = Tind[i-1, 2:]
    Tarr = np.zeros((len(terminii), 3), dtype=np.float32)
    Tarr[:, 0] = utils.compute_distances(x, Tind[:, :2])
    Tarr[:, 1] = utils.compute_angles(x, Tind[:, :3])
    Tarr[:, 2] = utils.compute_dihedrals(x, Tind)
    Tmat = np.zeros((len(terminii), 7), dtype=np.float32)
    Tmat[:, :4] = Tind
    Tmat[:, 4:] = Tarr
    return Tmat


def shave(x, tmat=None):
    """
    Shave terminal atoms off x

    Args:
        x: [natoms, 3] or [nframes, natoms, 3] array of coordinates
        tmat: optional, [nterminii, 7] array, the T-matrix. If not
            supplied, it is generated from analysis of x.

    Returns:
        xcore: [nframes, ncore, 3] array of core atom coordinates
        tmat: [nterminii, 7] array, the T-matrix
    """
    x = utils.check_dimensions(x, ensure_traj=True)
    one_frame = len(x) == 1
    n_tot = x.shape[1]
    if tmat is None:
        d = pdist(x[0])
        tmat = _make_tmat(x[0], d)
    terminii = tmat[:, 0].astype(np.int32)
    core = [i for i in range(n_tot) if i not in terminii]
    xcore = x[:, core]
    if one_frame:
        xcore = xcore[0]
    return xcore, tmat


def sprout(xcore, tmat):
    """
    Add terminal atoms to xcore

    Args:
        xcore: [natoms, 3] or [nframes, natoms, 3] array of core coordinates
        tmat: [nterminii, 7] array: the T-matrix

    Returns:
        xnew: [nframes, natoms, 3] array of completed coordinates.
    """
    xcore = utils.check_dimensions(xcore, ensure_traj=True)
    one_frame = len(xcore) == 1
    n_core = xcore.shape[1]
    n_frames = len(xcore)
    terminii = tmat[:, 0].astype(np.int32)
    n_terminii = len(terminii)
    n_all = n_core + n_terminii
    xnew = np.zeros((n_frames, n_all, 3), dtype=np.float32)
    core = [i for i in range(n_all) if i not in terminii]
    xnew[:, core] = xcore
    Hind = tmat[:, :4].astype(np.int32)
    Harr = tmat[:, 4:]
    for i in range(n_frames):
        for ijkl, rat in zip(Hind, Harr):
            local_axes = _get_local_axes(xnew[i, ijkl[1]], xnew[i, ijkl[2]],
                                         xnew[i, ijkl[3]])
            bond_vector = _get_bond_vector(rat[0], rat[1], rat[2])
            disp_vector = np.array(np.dot(bond_vector, local_axes))
            xnew[i, ijkl[0]] = xnew[i, ijkl[1]] + disp_vector
    if one_frame:
        xnew = xnew[0]
    return xnew

# methods for Triangulate:


def make_zmat(xf, xc):
    """
    Define positions of fine grained particles in xf
    by zmatrix based on cg particles xc
    """
    s = None
    for f, c in zip(xf, xc):
        d = cdist(f, c)
        if s is None:
            s = d
        else:
            s += d
    n = len(xf)
    mean = s / n
    ijkl = []
    ioff = mean.shape[1]
    for i, r in enumerate(d):
        ijkl.append([i + ioff] + list(np.argsort(r)[:3]))
    ijkl.sort(key=lambda x: x[1:])
    ijkl = np.array(ijkl)
    zarr = xyz2zmat(xf, xc, ijkl)
    zarrm = zarr.mean(axis=0)
    s = None
    for f in xf:
        d = pdist(f)
        if s is None:
            s = d
        else:
            s += d
    n = len(xf)
    mean = s / n
    ic = 0
    dmin = None
    for i, f in enumerate(xf):
        diff = pdist(f) - mean
        diff = (diff * diff).sum()
        if dmin is None:
            dmin = diff
        elif diff < dmin:
            dmin = diff
            ic = i

    zarrm[:, 2] = zarr[ic, :, 2]
    zmat = np.zeros((len(zarrm), 7))
    zmat[:, :4] = ijkl
    zmat[:, 4:] = zarrm
    return zmat


def xyz2zmat(xf, xc, z_indices):
    """
    Convert Cartesian coordinates in xf to Z-matrix based on xc.
    """
    nf = xf.shape[1]
    nc = xc.shape[1]
    n = xf.shape[0]
    x = np.zeros((n, nf+nc, 3))
    x[:, :nc] = xc
    x[:, nc:] = xf
    zarr = np.zeros((n, nf, 3))
    zarr[:, :, 0] = utils.compute_distances(x, z_indices[:, :2])
    zarr[:, :, 1] = utils.compute_angles(x, z_indices[:, :3])
    zarr[:, :, 2] = utils.compute_dihedrals(x, z_indices)
    zarr = np.nan_to_num(zarr)
    return zarr


def triangulate(xc, zmat):
    """
    Convert CG coordinates and a Z-matrix to FG Cartesian coordinates
    """
    z_inds = zmat[:, :4].astype(np.int32)
    zarrm = zmat[:, 4:]
    n_atoms = len(zarrm)
    n_frames = len(xc)
    nc = xc.shape[1]
    coords = np.zeros((n_frames, n_atoms + nc, 3))
    coords[:, :nc] = xc

    for k in range(n_frames):
        for i in range(n_atoms):
            coords1 = coords[k, z_inds[i, 1]]
            coords2 = coords[k, z_inds[i, 2]]
            coords3 = coords[k, z_inds[i, 3]]
            local_axes = _get_local_axes(coords1, coords2, coords3)
            bond_vector = _get_bond_vector(zarrm[i, 0], zarrm[i, 1],
                                           zarrm[i, 2])
            disp_vector = np.array(np.dot(bond_vector, local_axes))
            coords[k, z_inds[i, 0]] = coords1 + disp_vector
    return coords[:, nc:]


class Shave(object):
    """
    A form of resolution transformer

    Transform molecules between a "shaved" state when all terminal
    atoms (atoms connected by just one bond to the rest of the structure)
    are discarded and the "sprouted" state when these are added back in.
    The method relies on calculating a Z-matrix for the "shaved" atoms which
    is used to rebuild them - maybe attached to a different core conformation.

    Once trained on a matched pair of higher and lower resolution models of
    a system, Shave can transform further samples between the two resolutions
    in either direction.

    The API is modelled on that used by ML methods in scipy and sklearn:

    Instantiate a transformer:

        transformer = Shave()

    Train a transformer (to shave a molecule):

        transformer.fit(Xtrain)

        where Xtrain[n_xparticles, 3] is an example of the higher-resolution
        structure.

    Apply a transformer X->Y ("shave"):

        Ypred = transformer.transform(Xtest)

    Apply the inverse transform ("sprout", adding missing atoms back in):

       Xpred = transformer.inverse_transform(Ytest)

    """
    def __init__(self):
        self.tmat = None
        self.n_core = None

    def fit(self, X):
        """
        Train a resolution transformer that maps from X to Y, and the reverse.

        Args:

            X: [n_xparticles, 3] or [nframes, n_xparticles, 3] array of
                coordinates
        """
        X = utils.check_dimensions(X, ensure_traj=True)[0]
        self.n_tot = len(X)
        xcore, tmat = shave(X)
        self.terminii = tmat[:, 0].astype(np.int32)
        self.n_core = len(xcore)
        self.core = [i for i in range(self.n_tot) if i not in self.terminii]
        self.tmat = tmat

    def get_state(self):
        """
        Get the transformer configuration as a dictionary

        """
        if self.tmat is None or self.n_core is None:
            raise RuntimeError("Error: transformer has not been trained")

        config = {
            'n_tot': self.n_tot,
            'tmat': self.tmat.tolist()
            }
        return config

    def set_state(self, config):
        """
        Load the transformer configuration from a dictionary

        """
        self.n_tot = config['n_tot']
        self.tmat = np.array(config['tmat'], dtype=np.float32)
        self.terminii = self.tmat[:, 0].astype(np.int32)
        self.n_core = self.n_tot - len(self.terminii)
        self.core = [i for i in range(self.n_tot) if i not in self.terminii]

    def transform(self, X):
        X = utils.check_dimensions(X)
        one_frame = len(X.shape) == 2
        if one_frame:
            X = X.reshape((1, -1, 3))
        if not X.shape[1] == self.n_tot:
            raise ValueError(f'Error: X must be shape [Any, {self.n_tot}, 3]')

        Y = X[:, self.core]
        if one_frame:
            Y = Y[0]
        return Y

    def inverse_transform(self, Y):
        Y = utils.check_dimensions(Y)
        one_frame = len(Y.shape) == 2
        if one_frame:
            Y = Y.reshape((1, -1, 3))
        if not Y.shape[1] == self.n_core:
            raise ValueError(f'Error: Y must be shape [Any, {self.n_core}, 3]')
        X = [sprout(y, self.tmat) for y in Y]
        if one_frame:
            X = X[0]
        return np.array(X)


class Triangulate(object):
    """
    Determine positions of a set coordinates by triangulation from
    positions of another set

    """
    def __init__(self):
        self.zmat = None

    def fit(self, xc, xf):
        self.zmat = make_zmat(xf, xc)

    def predict(self, xc):
        return triangulate(xc, self.zmat)


class Glimps(object):
    """
    A resolution transformer

    Glimps is a machine learning approach to resolution transformation
    targetted primarily at molecular structures (sets of 3D coordinates).

    Once trained on a matched set of higher and lower resolution models of
    a system, Glimps can transform further samples between the two resolutions
    in either direction.

    The API is modelled on that used by ML methods in scipy and sklearn:

    Instantiate a transformer:

        transformer = Glimps()

    Train a transformer:

        transformer.fit(Xtrain, Ytrain)

        where Xtrain[n_samples, n_xparticles, 3] and
        Ytrain[n_samples, n_yparticles, 3] are matched pairs of structures
        at the two resolutions.

    Apply a transformer X->Y:

        Ypred = transformer.transform(Xtest)

    Apply the inverse transform:

       Xpred = transformer.inverse_transform(Ytest)

    At the core of the Glimps process is a simple multiple linear
    regression process, where coordinates (or their proxies) are transformed
    from one resolution to the other, but either side of this are a number of
    optional pre- and post-processing steps:

        a) MLR may be done using PCA scores rather than Cartesian coordinates.
        b) Positions of terminal atoms (those connected to the framework by
           a single bond) may be defined in internal coordinates ('shave' and
           'sprout' algorithm).
        c) An elastic network minimiser may be trained to improve geometry.
        d) Triangulation may replace the core MLR step.
    """

    def __init__(self, pca=False, refine=True, shave=True, triangulate=False):
        """
        Initiate a Glimps resolution transformer

        The pipeline depends on the options chosen. At the core is
        always the General Linear Model transformation, and the simplest
        mode just uses this:

            Xcg -> [GLM] -> Xfg (or the reverse, FG->CG)

        If PCA is included, it becomes:

            Xcg -> [PCA]->[GLM]->[PCA]-> Xfg

        If coordinate refinement is added it becomes:

            Xcg -> [GLM]->[ENM]-> Xfg

        etc., etc.

        Most pipelines work the same whether you are up-scaling
        or down-scaling, the exception is Sprout/Shave which only
        makes sense as part of an up-scaling pipeline.


        Args:
            pca: Bool, if True, use PCA transform step

            refine:    Bool, if True, use the TNC optimiser
                       to perform an elastic network type refinement

            shave:     Bool, if True, "shave" the high resolution structure
                       so positions of terminal atoms are calculated from a
                       Zmatrix.
            triangulate: Bool, if True, replace the core MLR step with the
                       triangulation method. If used, only the addition of
                       refine makes sense.
        """

        self.refine = refine
        self.shave = shave
        self.use_pca = pca
        self.triangulate = triangulate
        if triangulate:
            self.shave = False
            self.use_pca = False
        self.pca_x = None
        self.pca_y = None
        self.xy_trangulator = None
        self.yx_triangulator = None
        self.x_shaver = None
        self.y_shaver = None
        self.x_fitter = None
        self.y_fitter = None
        self.x_refiner = None
        self.y_refiner = None
        self.xy_regressor = None
        self.yx_regressor = None
        self.n_components = None
        self.xy_score = None  # not currently used
        self.yx_score = None  # not currently used
        self.trained = False

    def _get_tr(self, traj, ref):
        """
        Return a list of translation vectors and rotation matrices
        to map x onto ref
        """

        n = len(traj)
        trans = np.zeros((n, 3))
        rot = np.zeros((n, 3, 3))
        for i, x in enumerate(traj):
            rot[i], trans[i] = rv(x, ref)
        return trans, rot

    def _apply_tr(self, traj, t, r, inverse=False):
        """
        Apply translations and rotations to snapshots in traj.
        """
        result = np.zeros_like(traj)
        for i, x in enumerate(traj):
            if inverse:
                result[i] = (x - t[i]).dot(r[i].T)
            else:
                result[i] = x.dot(r[i]) + t[i]
        return result

    def fit(self, X, Y):
        """
        Train a resolution transformer that maps from X to Y, and the reverse.

        Args:

            X: [n_samples, n_xparticles, 3] array of coordinates
            Y: [n_samples, n_yparticles, 3] array of coordinates

        """
        X = utils.check_dimensions(X, ensure_traj=True)
        Y = utils.check_dimensions(Y, ensure_traj=True)
        if not len(X) == len(Y):
            raise ValueError('Error: X and Y must be matched samples')

        shape_x = X.shape
        shape_y = Y.shape
        self.upscaling = shape_x[1] < shape_y[1]

        if self.shave:
            if self.upscaling:
                self.y_shaver = Shave()
                self.y_shaver.fit(Y)
                Y = self.y_shaver.transform(Y)
                shape_y = Y.shape
            else:
                self.x_shaver = Shave()
                self.x_shaver.fit(X)
                X = self.x_shaver.transform(X)
                shape_x = X.shape

        if self.use_pca:
            self.n_components = min(len(X), shape_x[1] * 3, shape_y[1] * 3)
            if self.n_components < 2:
                raise ValueError('Error: insufficient samples for fitting')

            self.pca_x = PCA(n_components=self.n_components)
            self.pca_y = PCA(n_components=self.n_components)
            self.pca_x.fit(X)
            self.pca_y.fit(Y)
        else:
            self.x_fitter = utils.Procrustes()
            self.y_fitter = utils.Procrustes()
            self.x_fitter.fit(X)
            self.y_fitter.fit(Y)

        if self.refine:
            self.x_refiner = ENM()
            self.x_refiner.fit(X)
            self.y_refiner = ENM()
            self.y_refiner.fit(Y)

        if self.use_pca:
            x_scores = self.pca_x.transform(X)
            y_scores = self.pca_y.transform(Y)
        elif self.triangulate:
            x_scores = self.x_fitter.transform(X)
            y_scores = self.y_fitter.transform(Y)
        else:
            x_scores = self.x_fitter.transform(X).reshape((len(X), -1))
            y_scores = self.y_fitter.transform(Y).reshape((len(Y), -1))
        if self.triangulate:
            self.xy_triangulator = Triangulate()
            self.xy_triangulator.fit(x_scores, y_scores)
            self.yx_triangulator = Triangulate()
            self.yx_triangulator.fit(y_scores, x_scores)
        else:
            self.xy_regressor = LinearRegression().fit(x_scores, y_scores)
            self.yx_regressor = LinearRegression().fit(y_scores, x_scores)
        self.trained = True

    def get_state(self):
        """
        Get the state of the transformer as a dictionary

        """
        if not self.trained:
            raise RuntimeError("Error - the transformer has not been trained")
        config = {}
        for key in ['trained', 'refine', 'shave', 'use_pca',
                    'triangulate', 'n_components']:
            config[key] = self.__dict__[key]
        for key in ['x_shaver', 'y_shaver',
                    'x_fitter', 'y_fitter',
                    'x_refiner', 'y_refiner',
                    'pca_x', 'pca_y']:
            if self.__dict__[key] is None:
                config[key] = None
            else:
                config[key] = self.__dict__[key].get_state()
        for key in ['xy_regressor', 'yx_regressor']:
            if self.__dict__[key] is None:
                config[key] = None
            else:
                conf2 = {}
                for key2 in self.__dict__[key].__dict__:
                    if isinstance(self.__dict__[key].__dict__[key2], np.ndarray):
                        conf2[key2] = self.__dict__[key].__dict__[key2].tolist()
                    else:
                        conf2[key2] = self.__dict__[key].__dict__[key2]
                config[key] = conf2
        return config

    def set_state(self, config):
        """
        Set the state of the transformer from a dictionary

        """
        for key in ['trained', 'refine', 'shave', 'use_pca',
                    'triangulate', 'n_components']:
            self.__dict__[key] = config[key]
        for key in ['x_shaver', 'y_shaver']:
            if config[key] is None:
                self.__dict__[key] = None
            else:
                self.__dict__[key] = Shave()
                self.__dict__[key].set_state(config[key])
        for key in ['pca_x', 'pca_y']:
            if config[key] is None:
                self.__dict__[key] = None
            else:
                self.__dict__[key] = PCA()
                self.__dict__[key].set_state(config[key])
        for key in ['x_fitter', 'y_fitter']:
            if config[key] is None:
                self.__dict__[key] = None
            else:
                self.__dict__[key] = utils.Procrustes()
                self.__dict__[key].set_state(config[key])
        for key in ['x_refiner', 'y_refiner']:
            if config[key] is None:
                self.__dict__[key] = None
            else:
                self.__dict__[key] = ENM()
                self.__dict__[key].set_state(config[key])
        for key in ['xy_regressor', 'yx_regressor']:
            if config[key] is None:
                self.__dict__[key] = None
            else:
                self.__dict__[key] = LinearRegression()
                for key2 in config[key]:
                    if isinstance(config[key][key2], list):
                        config[key][key2] = np.array(config[key][key2],
                                                     dtype=np.float32)
                    self.__dict__[key].__dict__[key2] = config[key][key2]

    def transform(self, X):
        """
        Transform X to the resolution of Y

        Args:

            X: [n_samples, n_xparticles, 3] array of coordinates.

        Returns:

            Y: [n_samples, n_yparticles, 3] array of coordinates.
        """
        if self.xy_regressor is None and self.xy_triangulator is None:
            raise RuntimeError('Error: model has not been trained yet')

        X = utils.check_dimensions(X)
        one_frame = len(X.shape) == 2
        if one_frame:
            X = X.reshape((1, -1, 3))
        if self.x_shaver is not None:
            X = self.x_shaver.transform(X)
        if self.use_pca:
            if X.shape[1] != self.pca_x.n_atoms:
                n_found = X.shape[1]
                n_expected = self.pca_x.n_atoms
                raise ValueError(f'Error: X contains {n_found} atoms,'
                                 f' was expecting {n_expected}')
            t, r = self._get_tr(X, self.pca_x.mean)
            x_scores = self.pca_x.transform(X)
            y_scores = self.xy_regressor.predict(x_scores)
            Y = self.pca_y.inverse_transform(y_scores)
        else:
            if X.shape[1] != self.x_fitter.mean.shape[0]:
                n_found = X.shape[1]
                n_expected = self.x_fitter.mean.shape[0]
                raise ValueError(f'Error: X contains {n_found} atoms,'
                                 f' was expecting {n_expected}')
            t, r = self._get_tr(X, self.x_fitter.mean)
            if self.triangulate:
                x_scores = self.x_fitter.transform(X)
                Y = self.xy_triangulator.predict(x_scores)
            else:
                x_scores = self.x_fitter.transform(X).reshape((len(X), -1))
                y_scores = self.xy_regressor.predict(x_scores)
                Y = y_scores.reshape((len(X), -1, 3))
        if self.refine:
            Y = self.y_refiner.transform(Y)
        Y = self._apply_tr(Y, t, r, inverse=True)
        if self.y_shaver is not None:
            Y = self.y_shaver.inverse_transform(Y)
        if one_frame:
            Y = Y[0]
        return Y

    def inverse_transform(self, Y):
        """
        Transform Y to the resolution of X

        Args:

            Y: [n_samples, n_yparticles, 3] array of coordinates.

        Returns:

            X: [n_samples, n_xparticles, 3] array of coordinates.
        """
        if self.yx_regressor is None and self.yx_triangulator is None:
            raise RuntimeError('Error: model has not been trained yet')

        Y = utils.check_dimensions(Y)
        one_frame = len(Y.shape) == 2
        if one_frame:
            Y = Y.reshape((1, -1, 3))
        if self.y_shaver is not None:
            Y = self.y_shaver.transform(Y)
        if self.use_pca:
            if Y.shape[1] != self.pca_y.n_atoms:
                n_found = Y.shape[1]
                n_expected = self.pca_y.n_atoms
                raise ValueError(f'Error: Y contains {n_found} atoms,'
                                 f'was expecting {n_expected}')
            t, r = self._get_tr(Y, self.pca_y.mean)
            y_scores = self.pca_y.transform(Y)
            x_scores = self.yx_regressor.predict(y_scores)
            X = self.pca_x.inverse_transform(x_scores)
        else:
            if Y.shape[1] != self.y_fitter.mean.shape[0]:
                n_found = Y.shape[1]
                n_expected = self.y_fitter.mean.shape[0]
                raise ValueError(f'Error: Y contains {n_found} atoms,'
                                 f'was expecting {n_expected}')
            t, r = self._get_tr(Y, self.y_fitter.mean)
            if self.triangulate:
                y_scores = self.y_fitter.transform(Y)
                X = self.yx_triangulator.predict(y_scores)
            else:
                y_scores = self.y_fitter.transform(Y).reshape((len(Y), -1))
                x_scores = self.yx_regressor.predict(y_scores)
                X = x_scores.reshape((len(Y), -1, 3))

        if self.refine:
            X = self.x_refiner.transform(X)
        X = self._apply_tr(X, t, r, inverse=True)
        if self.x_shaver is not None:
            X = self.x_shaver.inverse_transform(X)
        if one_frame:
            X = X[0]
        return X
