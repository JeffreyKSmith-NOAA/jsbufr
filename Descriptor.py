import array
from BUFRConstants import *

class Descriptor:

    def __init__(self, fxy):

        if isinstance(fxy, str):
            self.f = int(fxy[0])
            self.x = int(fxy[1:3])
            self.y = int(fxy[3:])
        else:
            self.f = fxy[0] >> 6
            self.x = fxy[0] & 0x3f
            self.y = fxy[1]

        self.sub_descriptors = []

        return

    def fxy_string(self):
        return "%1d%02d%03d" % (self.f, self.x, self.y)

    def tableB_string(self):
        return "%1d-%02d-%03d" % (self.f, self.x, self.y)

    def expand_sequence(self, tableD):

        for desc in tableD[self.fxy_string()].descriptors:
            self.sub_descriptors.append(Descriptor.Descriptor(desc))
            if desc.f == 3:
                desc.expand_sequence(tableD)

        return

    def __repr__(self):

        return "f=%d, x=%d, y=%d " % (self.f, self.x, self.y)
