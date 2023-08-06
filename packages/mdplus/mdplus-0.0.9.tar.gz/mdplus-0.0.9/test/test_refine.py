import os
import numpy as np
import pytest
from mdplus import refinement
from mdplus.utils import rmsd

rootdir = os.path.dirname(os.path.abspath('__file__'))
catrajdat = os.path.join(rootdir, 'examples/test_ca.npy')
trajdat = os.path.join(rootdir, 'examples/test.npy')

@pytest.fixture(scope="module")
def catraj():
    t =  np.load(catrajdat)
    return t

@pytest.fixture(scope="module")
def traj():
    t =  np.load(trajdat)
    return t

def test_optimize_fit(catraj):
    r = refinement.ENM()
    r.fit(catraj)
    assert r.n_atoms == 58
    assert len(r.restraints) == 113

def test_optimize_transform(catraj):
    r = refinement.ENM()
    r.fit(catraj)
    ref = catraj[0]
    crude = ref + (np.random.random(ref.shape) * 0.02) - 0.01 
    refined = r.transform(crude)

def test_fix_bumps(traj):
    x = traj[0]
    x2 = x + np.random.random((x.shape)) * 0.1 - 0.5
    x3 = refinement.fix_bumps(x2, 0.1, 0.15)

