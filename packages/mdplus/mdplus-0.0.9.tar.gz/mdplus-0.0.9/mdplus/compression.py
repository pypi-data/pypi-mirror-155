import xdrlib
import traceback
import numpy as np
from mdplus.utils import squeeze, stretch

class SQZFileReader(object):
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.unpacker = xdrlib.Unpacker(self.file.read())
        self.eof = False
        self.framecount = 0
    
    def __del__(self):
        try:
            self.file.close()
        except:
            pass
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        self.close()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        return True
        
    def close(self):
        self.file.close()

    def read(self):
        xyz = []
        unitcell_lengths = []
        unitcell_angles = []
        time = []
        for c, l, a, t in self.read_frames():
            xyz.append(c)
            unitcell_lengths.append(l)
            unitcell_angles.append(a)
            time.append(t)
        return np.array(xyz), np.array(unitcell_lengths), np.array(unitcell_angles), np.array(time)
                
    def read_frames(self):
        self.eof = False
        try:
            c, l, a, t = self.read_frame()
        except EOFError:
            self.eof = True
        while not self.eof:
            yield c, l, a, t
            try:
                c, l, a, t = self.read_frame()
            except EOFError:
                self.eof = True
            
    def read_frame(self):
        b = self.unpacker.unpack_bytes()
        d = stretch(b)
        if self.framecount == 0:
            l = len(d)
            self.natoms = (l-7) // 3
            self.buff0 = np.zeros(l, dtype=np.int32)
            self.buff1 = np.zeros(l, dtype=np.int32)
            self.buff2 = np.zeros(l, dtype=np.int32)
        self.buff2[:] = d
        if self.framecount == 0:
            self.buff1[:] = self.buff2
            self.buff0[:] = self.buff1
        elif self.framecount == 1:
            self.buff1[:] = self.buff2
            self.buff0 += self.buff1
        else:
            self.buff1 += self.buff2
            self.buff0 += self.buff1
        rdata = self.buff0 / 1000
        self.framecount += 1

        coordinates = rdata[:3*self.natoms]
        unitcell_lengths = rdata[3*self.natoms: 3*self.natoms+3]
        unitcell_angles = rdata[3*self.natoms+3: 3*self.natoms+6]
        time = rdata[-1]
        return coordinates.reshape((self.natoms, 3)), unitcell_lengths, unitcell_angles, time

class SQZFileWriter(object):
    def __init__(self, filename):
        self.file = open(filename, 'wb')
        self.packer = xdrlib.Packer()
        self.framecount = 0
    
        def __del__(self):
            try:
                self.close()
            except:
                pass
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        self.close()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        return True
        
    def close(self):
        self.file.write(self.packer.get_buffer())
        self.file.close()
    
    def write_frame(self, crds, unitcell_lengths, unitcell_angles, time):
        if self.framecount == 0:
            self.natoms = len(crds)
            l = 3 * self.natoms + 7
            self.buff0 = np.zeros(l, dtype=np.int32)
            self.buff1 = np.zeros(l, dtype=np.int32)
            self.buff2 = np.zeros(l, dtype=np.int32) 
        data = np.concatenate((crds.flatten(), unitcell_lengths, unitcell_angles, [time]))
        self.buff2[:] = self.buff1
        self.buff1[:] = self.buff0
        self.buff0 = np.rint(data * 1000).astype(np.int32)
        if self.framecount == 0:
            ix = self.buff0
        elif self.framecount == 1:
            ix = self.buff0 - self.buff1
        else:
            ix = self.buff0 - 2 * self.buff1 + self.buff2
        self.packer.pack_bytes(squeeze(ix))
        self.framecount += 1
    
    def write_frames(self, crds, unitcell_lengths, unitcell_angles, time):
        for c, l, a, t in zip(crds, unitcell_lengths, unitcell_angles, time):
            self.write_frame(c, l, a, t)
        
