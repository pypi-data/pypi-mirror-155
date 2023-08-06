import os
import numpy as np
import pytest
from mdplus import pca
from mdplus.utils import rmsd

rootdir = os.path.dirname(os.path.abspath('__file__'))
trajfile = os.path.join(rootdir, 'examples/test_ca.npy')

@pytest.fixture(scope="module")
def traj():
    t =  np.load(trajfile)
    return t

def test_fit(traj):
    p = pca.PCA(n_components=0.9)
    p.fit(traj)
    assert p.n_atoms == 58
    assert p.n_components == 7

def test_fit_transform(traj):
    p = pca.PCA(n_components=0.9)
    projs = p.fit_transform(traj)
    assert p.n_atoms == 58
    assert p.n_components == 7
    assert projs.shape[1] == p.n_components

def test_fit_transform_inverse_transform(traj):
    p = pca.PCA()
    projs = p.fit_transform(traj)
    newxyz = p.inverse_transform(projs)
    for i in range(len(newxyz)):
        assert rmsd(traj[i],  newxyz[i]) < 0.02

def test_fit_transform_nofit(traj):
    p = pca.PCA(n_components=0.9, procrustes=False)
    projs = p.fit_transform(traj)
    assert p.n_atoms == 58
    assert p.n_components == 6
    assert projs.shape[1] == p.n_components

