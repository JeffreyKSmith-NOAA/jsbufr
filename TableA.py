import re

from BUFRConstants import *

DESCRIPTOR_PATTERN = "^  0-\d\d-\d\d\d"

class TableAEntry:
    def __init__(self, mnemonic, description):
        self.mnemonic = mnemonic
        self.description = description
        return

    def __repr__(self):
        return "%s %s" % (self.mnemonic, self.description)


class TableA(dict):
    def __init__(self):

        pass

        return


    def extend_table(self, tableMessage):

        idx = 1
        print "There are ", tableMessage[idx-1], " Table A entries"
        for i in range(tableMessage[idx-1]):
            descriptorCode = chr(tableMessage[idx+]) + \
                             tableMessage[idx+:idx+].tostring() + \
                             tableMessage[idx+:idx|].tostring()
            self[descriptorCode] = TableAEntry(tableMessage[:idx+], \
                                               tableMessage[idx+:idx+].strip())

            idx += 67

        return
