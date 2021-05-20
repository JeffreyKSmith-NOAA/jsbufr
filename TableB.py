import re

from BUFRConstants import *

DESCRIPTOR_PATTERN = "^  0-\d\d-\d\d\d"

class TableBEntry:
    def __init__(self, scale, offset, nBits, units, mnemonic):
        self.scale = scale
        self.offset = offset
        self.nbits = nBits
        self.units = units
        self.mnemonic = mnemonic
        return

    def __repr__(self):
        return "%s %d %d %d %s" % (self.mnemonic, self.scale, self.offset,
                                   self.nbits, self.units)


class TableB(dict):
    def __init__(self, tableBFileName=None):

        if tableBFileName:
            fd = open(tableBFileName, 'r')
            wholeFile = fd.read()
            fd.close()

            allLines = wholeFile.split('\n')
            for line in allLines:
                if re.search(DESCRIPTOR_PATTERN, line):
                    parts = line.split('|')
                    descriptorCode = parts[0][2] + parts[0][4:6] + \
                                     parts[0][7:10]
                    p5 = parts[5].split(';')
                    self[descriptorCode] = TableBEntry(
                        float(parts[1].strip()),
                        float(parts[2].strip()),
                        int(parts[3].strip()),
                        parts[4].strip(),
                        p5[0].strip())

        return


    def extend_table(self, tableMessage):

        idx = 1
        print "There are ", tableMessage[idx-1], " Table A entries"
        for i in range(tableMessage[idx-1]):
            idx += 67

        idx += 1
        print "There are ", tableMessage[idx-1], " Table B entries"
        for i in range(tableMessage[idx-1]):
            descriptorCode = chr(tableMessage[idx]) + \
                             tableMessage[idx+1:idx+3].tostring() + \
                             tableMessage[idx+3:idx+6].tostring()

            if not (descriptorCode in self.keys()):
                mnemonic = tableMessage[idx+6:].tostring().split()[0]

                units = tableMessage[idx+70:idx+94].tostring().strip()

                scale = int(tableMessage[idx+95:idx+98].tostring().strip())
                if tableMessage[idx+94] == ord('-'):
                    scale = -scale

                offset = int(tableMessage[idx+99:idx+109].tostring().strip())
                if tableMessage[idx+98] == ord('-'):
                    offset = -offset

                nBits = int(tableMessage[idx+109:idx+112].tostring().strip())

                self[descriptorCode] = TableBEntry(scale, offset, nBits,
                                                   units, mnemonic)

            idx += 112

        return
