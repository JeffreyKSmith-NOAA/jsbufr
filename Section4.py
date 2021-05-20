import array

from BUFRConstants import *

class Section4:

    def __init__(self, bufrFile, bufrEdition):

        block = array.array('B')
        block.fromfile(bufrFile, SECTION4_BASE_LENGTH)
        if block[0] == 55 and block[1] == 55 and block[2] == 55 and \
           block[3] == 55:
            bufrFile.seek(0 - SECTION4_BASE_LENGTH, 1)
            self.section_length = 0
            return
        self.section_length = BYTE_MULT*(BYTE_MULT*block[0] + block[1]) + \
                              block[2]

        block = array.array('B')
        block.fromfile(bufrFile, self.section_length - SECTION4_BASE_LENGTH)
        self.data_contents = block

        # sections begin on even numbered bytes, so if this section has an
        # odd length then need to read in a filler byte
        if bufrEdition == 3 and self.section_length & BIT_MASK[7]:
            block.fromfile(bufrFile, 1)
        
        return

    def extract(messageMap, mnemonic, index):

        candidates = [x for x in messageMap if x.mnemonic == mnemonic]
        wantedField = candidates[index-1]
        value = self.__bruteforce(wantedField.start_bit/8,
                                  wantedField.start_bit,
                                  wantedField.end_bit - 
                                  wantedField.start_bit - 1)

        return value

    def __bruteForce(bytePtr, bitPtr, nBits):

        value = 0
        for i in range(nBits):
            if self.data_content[bytePtr] & BIT_MAP[bitPtr % 8]:
                value = 2*value + 1
            else:
                value = 2*value
            bitPtr += 1
            if bitPtr == 8:
                bitPtr = 0
                bytePtr += 1

        return value

    def __repr__(self):
        return "data section length = %d" % (self.section_length,)
