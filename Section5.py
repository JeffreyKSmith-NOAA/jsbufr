import array

from BUFRConstants import *

class Section5:
    def __init__(self, bufrFile):

        block = array.array('c')
        block.fromfile(bufrFile, SECTION5_LENGTH)

        self.the_end = ''.join(block.tolist())

        return

    def __repr__(self):

        return self.the_end


