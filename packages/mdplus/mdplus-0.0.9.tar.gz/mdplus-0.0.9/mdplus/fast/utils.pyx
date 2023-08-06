##############################################################################
# Imports
##############################################################################

import numpy as np

cimport cython
cimport numpy as np

##############################################################################
# External Declarations
##############################################################################

cdef extern from "matfit.c":
    int matfitw(const long n_atoms, const float *xa, const float *xb,
                float *r, float *v, float *rmse,
                const int dofit, const float *w)

cdef extern from "fitutil.c":
    int fit_frame(const long n_atoms, const float *in_frame,
                  const float *r, const float *v, float *out_frame)

    int fast_pib(const long n_atoms, const float *in_coords,
                 const float *box, float *out_coords)

##############################################################################
# Public Functions
##############################################################################

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bumps(float [:, :] x, int [:, :] ij, float dmin):
    """
    Find distances in x that are less than dmin

    Returns the number of bumps found: if this is equal to
    the length of ij it's a flag that there may be more.

    """
    cdef Py_ssize_t n_atoms = x.shape[0]
    cdef Py_ssize_t max_bumps = ij.shape[0]
    
    cdef Py_ssize_t i, j
    cdef int nbumps
    cdef float dx, dy, dz, r, dmin2
    
    dmin2 = dmin * dmin
    nbumps = 0
    
    for i in range(n_atoms - 1):
        for j in range(i +1, n_atoms):
            dx = x[i, 0] - x[j, 0]
            dx = dx * dx
            if dx < dmin2:
                dy = x[i, 1] - x[j, 1]
                dy = dy * dy
                if dy < dmin2:
                    dz = x[i, 2] - x[j, 2]
                    dz = dz * dz
                    if dz < dmin2:
                        r = dx + dy + dz
                        if r < dmin2:
                            ij[nbumps, 0] = i
                            ij[nbumps, 1] = j
                            nbumps += 1
                            if nbumps >= max_bumps:
                                return nbumps
    return nbumps

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef fitted_traj(traj, ref, w=None):
    """
    Fast fitting function. Fits every snapshot in traj
    to structure ref and returns the transformed coordinates

    An optional array of weights may be provided.
    """

    cdef int dofit
    cdef long f
    cdef long n_frames = traj.shape[0]
    cdef long n_atoms = traj.shape[1]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame
    cdef float[:, :, :] out_traj

    dofit = 1

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)
    out_traj = np.asarray(np.zeros([n_frames, n_atoms, 3]), order='C', dtype=np.float32)

    for f in range(n_frames):
        in_frame = np.asarray(traj[f, :, :], order='C', dtype=np.float32)

        matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])
        fit_frame(n_atoms, &in_frame[0,0], &r[0,0], &v[0], &out_traj[f, 0, 0])

    return np.array(out_traj, dtype=np.float32)

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef fitted(in_, ref, w=None):
    """
    Fits in_ to structure ref and returns the
    the resulting coordinates

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long n_atoms = in_.shape[0]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame
    cdef float[:, :] out_frame

    dofit = 1

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    in_frame = np.asarray(in_, order='C', dtype=np.float32)
    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)
    out_frame = np.asarray(np.zeros([n_atoms, 3]), order='C', dtype=np.float32)

    matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])
    fit_frame(n_atoms, &in_frame[0,0], &r[0,0], &v[0], &out_frame[0,0])

    return np.array(out_frame, dtype=np.float32)



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef rv(in_, ref, w=None):
    """
    Fits in_ to structure ref and returns the
    the rotation matrix and shift vector.

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long n_atoms = in_.shape[0]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame

    dofit = 1

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    in_frame = np.asarray(in_, order='C', dtype=np.float32)
    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)

    matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])

    return np.array(r, dtype=np.float32), np.array(v, dtype=np.float32)



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef rmsd_traj(traj, ref, w=None):
    """
    Fits every snapshot in traj to structure ref and returns the
    the rmsd.

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long f
    cdef long n_frames = traj.shape[0]
    cdef long n_atoms = traj.shape[1]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:] out_rms
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame

    dofit = 0

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)
    out_rms = np.asarray(np.zeros([n_frames]), order='C', dtype=np.float32)

    for f in range(n_frames):
        in_frame = np.asarray(traj[f, :, :], order='C', dtype=np.float32)

        matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])
        out_rms[f] = rms

    return np.array(out_rms, dtype=np.float32)



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef rmsd(in_, ref, w=None):
    """
    Calculates the (optionally mass-weighted) rmsd between in_ and ref

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long n_atoms = in_.shape[0]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame

    dofit = 0

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    ref_frame = np.asarray(ref, order='C', dtype=np.float32)
    in_frame = np.asarray(in_, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)

    matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])

    return rms



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef fitted_mean(traj, ref, w=None):
    """
    Fits every snapshot in traj to structure ref and returns the
    the mean coordinates

    An optional array of weights may be provided
    """

    cdef int dofit
    cdef long f
    cdef long n_frames = traj.shape[0]
    cdef long n_atoms = traj.shape[1]

    cdef float rms = 0.0
    cdef float[:] wloc
    cdef float[:] v
    cdef float[:, :] r
    cdef float[:, :] in_frame
    cdef float[:, :] ref_frame
    cdef float[:, :] out_frame

    dofit = 1

    if w is None:
        wloc = np.asarray(np.ones([n_atoms]), order='C', dtype=np.float32)
    else:
        wloc = np.asarray(w[:, 0], order='C', dtype=np.float32)

    ref_frame = np.asarray(ref, order='C', dtype=np.float32)

    v = np.asarray(np.zeros([3]), order='C', dtype=np.float32)
    r = np.asarray(np.zeros([3, 3]), order='C', dtype=np.float32)
    out_frame = np.asarray(np.zeros([n_atoms, 3]), order='C', dtype=np.float32)

    for f in range(n_frames):
        in_frame = np.asarray(traj[f, :, :], order='C', dtype=np.float32)

        matfitw(n_atoms, &ref_frame[0,0], &in_frame[0,0], &r[0,0], &v[0], &rms, dofit, &wloc[0])
        fit_frame(n_atoms, &in_frame[0,0], &r[0,0], &v[0], &out_frame[0,0])

    out_frame = np.divide(out_frame, n_frames)
    return np.array(out_frame, dtype=np.float32)



@cython.boundscheck(False)
@cython.wraparound(False)
cpdef pib(coords, box):
    """
    Fast version of "pack into box" in utils.py
    Wraps coordinates into the primary unit cell
    """

    cdef long f
    cdef long n_frames = coords.shape[0]
    cdef long n_atoms = coords.shape[1]

    cdef float[:, :] in_coords
    cdef float[:, :] in_box
    cdef float[:, :, :] out_coords

    out_coords = np.asarray(np.zeros([n_frames, n_atoms, 3]), order='C', dtype=np.float32)

    for f in range(n_frames):
        in_coords = np.asarray(coords[f, :, :], order='C', dtype=np.float32)
        in_box = np.asarray(box[f, :, :], order='C', dtype=np.float32)

        fast_pib(n_atoms, &in_coords[0,0], &in_box[0,0], &out_coords[f,0,0])

    return np.array(out_coords, dtype=np.float32)

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
def fg(double [:] x, int [:,:] ij, float [:] d, float fc):
    """
    Force and gradient for an elastic network minimiser
    """
    cdef Py_ssize_t n = x.shape[0]
    cdef Py_ssize_t nk = ij.shape[0]
    cdef Py_ssize_t i, j, k, l, m
    
    G = np.zeros(n, dtype = np.float32)
    cdef float [:] G_view = G
    cdef float f, r2, r, fr, dr, gr, dx, lfc
    
    lfc = fc
    f = 0.0
    for k in range(nk):
        i = ij[k, 0] * 3
        j = ij[k, 1] * 3
        r2 = 0.0
        for l in range(3):
            dx = x[j+l] - x[i+l]
            r2 += dx * dx
        r = np.sqrt(r2)
        r = max(1.0e-6, r) # avoid divide by zero
        dr = r - d[k]
        fr = dr * dr * lfc
        gr = 2 * fc * dr / r
        for l in range(3):
            dx = x[j+l] - x[i+l]
            G_view[i+l] -= dx * gr
            G_view[j+l] += dx * gr
        f += fr
    return f, G
            

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
def make_dx(float [:,:] x, float [:] dd, long [:, :] ij, long [:] terminal):
    """
    REFINE utility function: Calculate the coordinate shift vector DX.

    Arguments:
        x: [N,3] numpy array of current coordinates.
        dd: [K] numpy array of bond length gradients
        ij: [K, 2] numpy array indexing atom pairs for each bond in dd
        terminal:[N] numpy array, 1 if atom is terminal (1 bond)
    Returns:
        [N, 3] numpy array of shifts (will be further processed in calling
        python function)
    """
    
    cdef Py_ssize_t n = x.shape[0]
    cdef Py_ssize_t nk = ij.shape[0]
    cdef Py_ssize_t i, j, k, l, m
    
    DX = np.zeros((n, 3), dtype = np.float32)
    cdef float [:, :] DX_view = DX
    cdef float dx
    
    for k in range(nk):
        i = ij[k, 0]
        j = ij[k, 1]
        m = terminal[i] + terminal[j]
        for l in range(3):
            dx = x[j, l] - x[i, l]
            dx = dx * dd[k]
            if m == 2 or terminal[i] == 0:
                DX_view[j, l] += dx
            if m == 2 or terminal[j] == 0:
                DX_view[i, l] -= dx
    return DX

#
# Squeeze and stretch utility for integer compression:
#

cdef unsigned int signbit(unsigned int a):
    cdef unsigned int v
    cdef unsigned int m = (1 << 31)
    v = (a & m) >> 31
    return v

cdef unsigned int invert(unsigned int a):
    cdef unsigned int m = (1 << 32) - 1
    return 1 + (a ^ m)

cdef unsigned int bit_length(unsigned int i):
    cdef unsigned int l
    l = 0
    while i != 0:
        i >>= 1
        l += 1
    return l

cdef unsigned int encode(unsigned int i):
    cdef unsigned int j
    j = signbit(i)
    if j == 1:
        i = invert(i)
    i <<= 1
    return i + j

cdef unsigned int decode(unsigned int i):
    cdef unsigned int j, k
    j = i & 1
    k = i
    k >>= 1
    if j == 1:
        k = invert(k)
    return k

#@cython.boundscheck(False)  # Deactivate bounds checking
#@cython.wraparound(False)   # Deactivate negative indexing.
cpdef put(unsigned int[:] buff, unsigned int[:] iptr, unsigned int v, unsigned int nbits):
    cdef Py_ssize_t ibyte, 
    cdef unsigned int ibit, headroom, overflow
    cdef unsigned int maxint, ipt
    
    ipt = iptr[0]
    ibyte = ipt // 32
    ibit = ipt % 32
    maxint = (1 << 32) - 1
    v &= ((1 << nbits) - 1)
    headroom = 32 - ibit
    if nbits <= headroom:
        v <<= ibit
        buff[ibyte] += v
    else:
        overflow = v >> headroom
        v <<= ibit
        buff[ibyte] += v & maxint
        buff[ibyte+1] = overflow
            
    iptr[0] = ipt + nbits

#@cython.boundscheck(False)  # Deactivate bounds checking
#@cython.wraparound(False)   # Deactivate negative indexing.
cpdef get(unsigned int[:] buff, unsigned int[:] iptr, unsigned int[:] v, unsigned int nbits):
    cdef Py_ssize_t ibyte
    
    cdef unsigned int ibit, headroom, overflow
    cdef unsigned int mask, v1, v2, ipt
    
    ipt = iptr[0]
    ibyte = ipt // 32
    ibit = ipt % 32
    headroom = 32 - ibit
    if nbits < headroom:
        mask = ((1 << (ibit + nbits)) - 1)
        v1 = buff[ibyte] & mask
        v1 >>= ibit
        v[0] = v1
    else:
        overflow = nbits - headroom
        v1 = buff[ibyte] >> ibit
        mask = (1 << overflow) - 1
        v2 = buff[ibyte+1] & mask
        v2 <<= headroom
        v[0] = v1 + v2
    iptr[0] = ipt + nbits

#@cython.boundscheck(False)  # Deactivate bounds checking
#@cython.wraparound(False)   # Deactivate negative indexing.
def pack(unsigned int[:] iarr):
    cdef unsigned int il = iarr.shape[0]
    buff = np.zeros(il, dtype=np.uint32)
    bl = np.zeros(il, dtype=np.uint32)
    iptr = np.zeros(1, dtype=np.uint32)
    
    cdef unsigned int[:] buff_view = buff
    cdef unsigned int[:] bl_view = bl
    cdef unsigned int[:] iptr_view = iptr
    cdef Py_ssize_t  i, j
    
    cdef unsigned int v, l, m

    iptr_view[0] = 0
    for i in range(il):
        #v = encode(iarr[i])
        v = iarr[i]
        l = bit_length(v)
        bl_view[i] = l
        if l > 0:
            m = (1 << (l - 1)) - 1
            v = v & m
            l -= 1
            put(buff_view, iptr_view, v, l)
    j = iptr_view[0] // 32
    return buff[:j+2], bl

#@cython.boundscheck(False)  # Deactivate bounds checking
#@cython.wraparound(False)   # Deactivate negative indexing.
def unpack(unsigned int[:] buff, unsigned int[:] bl):
    cdef Py_ssize_t il = bl.shape[0]
    iout = np.zeros(il, dtype=np.uint32)
    cdef unsigned int[:] iout_view = iout
    iptr = np.zeros(1, dtype=np.uint32)
    v = np.zeros(1, dtype=np.uint32)
    cdef unsigned int[:] iptr_view = iptr
    cdef unsigned int[:] v_view = v
    cdef Py_ssize_t i
    cdef unsigned int l, m
    
    iptr_view[0] = 0
    for i in range(il):
        l = bl[i]
        if l > 0:
            l -= 1
            get(buff, iptr_view, v_view, l)
            m = 1 << (l)
            v_view[0] += m
            #iout_view[i] = decode(v_view[0])
            iout_view[i] = v_view[0]
    return iout
