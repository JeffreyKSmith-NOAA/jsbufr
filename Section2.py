import array

from BUFRConstants import *

class Section2:

    def __init__(self, bufrFile, bufrEdition):

        block = array.array('B')
        block.fromfile(bufrFile, SECTION2_BASE_LENGTH)
        print("block = ", block)

        self.section_length = BYTE_MULT*(BYTE_MULT*block[0] + block[1]) + \
                              block[2]

        # if there actually is a section 2, then it is likely to be more
        # than 4 bytes long
        if self.section_length > SECTION2_BASE_LENGTH:
            block.fromfile(bufrFile,
                           self.section_length - SECTION2_BASE_LENGTH)

        # sections begin on even numbered bytes, so if Section 2 had an odd
        # length then need to read in a filler byte
        if bufrEdition == 3 and (self.section_length & BIT_MASK[7]):
            block.fromfile(bufrFile, 1)

        return

    def __repr__(self):

        return "length of Section 2 = %d" % (self.section_length,)

