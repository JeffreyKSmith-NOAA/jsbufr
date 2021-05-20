import array

from BUFRConstants import *
import Descriptor

class Section3:

    def __init__(self, bufrFile, bufrEdition):

        block = array.array('B')
        block.fromfile(bufrFile, SECTION3_BASE_LENGTH)
        self.section_length = BYTE_MULT*(BYTE_MULT*block[0] + block[1]) + \
                              block[2]
        self.num_subsets = BYTE_MULT*block[4] + block[5]
        self.observed_data = block[6] & BIT_MASK[0]
        self.compressed_data = block[6] & BIT_MASK[1]

        block = array.array('B')
        block.fromfile(bufrFile, self.section_length - SECTION3_BASE_LENGTH)
        self.descriptors = []
        nDescriptors = len(block)//2
        for i in range(nDescriptors):
            self.descriptors.append(
                Descriptor.Descriptor(block[2*i:2*(i + 1)]))

        # sections begin on even numbered bytes, so if the section has an
        # odd length then need to read in a filler byte
        if bufrEdition == 3 and self.section_length & BIT_MASK[7]:
            block.fromfile(bufrFile, 1)

        return

    def __repr__(self):
        msg = "section length = %d, number of subsets = %d" % \
            (self.section_length, self.num_subsets)
        if self.observed_data:
            msg += ", observed data"
        if self.compressed_data:
            msg += ", compressed data"
        msg += "\n%s" % (self.descriptors,)
        return msg
