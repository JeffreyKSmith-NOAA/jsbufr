import array

from BUFRConstants import *

class Section0:

    def __init__(self, bufrFile):

        block = array.array('c')
        block.fromfile(bufrFile, 4)
        
        self.bufr = block[0] + block[1] + block[2] + block[3]

        block = array.array('B')
        block.fromfile(bufrFile, 3)
        self.message_length = BYTE_MULT*(BYTE_MULT*block[0] + block[1]) + \
                              block[2]
                                        
        block = array.array('B')
        block.fromfile(bufrFile, 1)
        self.edition_number = block[0]

        return


    def __repr__(self):

        return "message length = %d, edition number = %d   %s" % \
            (self.message_length, self.edition_number, self.bufr)
