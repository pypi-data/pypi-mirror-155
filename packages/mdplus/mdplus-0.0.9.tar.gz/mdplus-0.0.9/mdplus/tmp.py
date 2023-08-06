def zagzig_encode(iarr):
    iarr = np.array(iarr, dtype=np.int32)
    sign = np.abs((np.sign(iarr)-1)//2)
    iarr = (np.abs(iarr)*2 + sign).astype(np.uint32)
    return iarr

def zagzig_decode(iarr):
    iarr = np.array(iarr, dtype=np.uint32)
    neg = iarr % 2 == 1
    iarr = (iarr // 2).astype(np.int32)
    iarr = np.where(neg, -iarr, iarr)
    return iarr

def squeeze(ilist):
    iarr = np.array(ilist).flatten()
    signed = iarr.min() < 0
    if signed:
        iarr = zagzig_encode(iarr)
    else:
        iarr = iarr.astype(np.uint32)
    buff, bl = fast.pack(iarr)
    buff = buff.tobytes()
    bl = bl.astype(np.uint8)
    blz = zlib.compress(bl)
    lb = len(buff)
    if signed:
        lb = -lb
    off = np.array([lb], dtype=np.int32).tobytes()
    return off + buff + blz

def stretch(sq):
    off = np.frombuffer(sq[:4], dtype=np.int32)[0]
    signed = off < 0
    if signed:
        off = -off
    buff = np.frombuffer(sq[4:4+off], dtype=np.uint32).copy()
    blz = sq[4+off:]
    bl = np.frombuffer(zlib.decompress(blz), dtype=np.uint8).astype(np.uint32)
    iout = fast.unpack(buff, bl)
    if signed:
        iout = zagzig_decode(iout)
    return iout.astype(np.int32)
