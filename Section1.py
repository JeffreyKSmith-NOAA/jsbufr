import array

from BUFRConstants import *

class Section1:

    def __init__(self, bufrFile, bufrEdition):

        block = array.array('B')
        block.fromfile(bufrFile, 3)
        print(block)

        self.section_length = BYTE_MULT*(BYTE_MULT*block[0] + block[1]) + \
                              block[2]

        # NOTE: this appends to block. It does not overwrite the existing
        #       contents
        block.fromfile(bufrFile, self.section_length - 3)
        if bufrEdition == 3:
            self.master_table = block[3]
            self.orig_subcenter = block[4]
            self.orig_center = block[5]
            self.update_sequence_number = block[6]
            self.optional_section_flag = block[7]
            self.generating_center = block[8]
            self.message_subtype = block[9]
            self.master_table_version = block[10]
            self.local_table_version = block[11]
            self.year = block[12]
            self.month = block[13]
            self.day = block[14]
            self.hour = block[15]
            self.minute = block[16]
        elif bufrEdition == 4:
            self.master_table = block[3]
            self.orig_subcenter = BYTE_MULT*block[4] + block[5]
            self.orig_center = BYTE_MULT*block[6] + block[7]
            self.update_sequence_number = block[8]
            self.optional_section_flag = block[9]
            self.generating_center = block[10]
            self.international_subtype = block[11]
            self.local_subtype = block[12]
            self.master_table_version = block[13]
            self.local_table_version = block[14]
            self.year = BYTE_MULT*block[15] + block[16]
            self.month = block[17]
            self.day = block[18]
            self.hour = block[19]
            self.minute = block[20]
            self.second = block[21]

        # a section must have an even number of bytes. If
        # self.section_length is odd, there should be a filler byte before the
        # next section
        if bufrEdition == 3 and self.section_length & BIT_MASK[7]:
            block.fromfile(bufrFile, 1)

        return

    def __repr__(self):

        return "length = %d, master table = %d, center = %d-%d, date=%d/%d/%d time = %d:%d" % (self.section_length, self.master_table, self.orig_center, self.orig_subcenter, self.month, self.day, self.year, self.hour, self.minute)
