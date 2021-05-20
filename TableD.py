import re

SEQUENCE_PATTERN = "^  3-[0-9]{2}-[0-9]{3} \|"
DESCRIPTOR_PATTERN = "^           \| [0-3]-[0-9]{2}-[0-9]{3}"

class TableDEntry:
    def __init__(self, mnemonic):

        self.mnemonic = mnemonic
        self.descriptors = []

        return

    def __repr__(self):
        return "%s %d" % (self.mnemonic, len(self.descriptors))

class TableD(dict):
    def __init__(self, tableDFileName=None):

        if tableDFileName:
            fd = open(tableDFileName, 'r')
            wholeFile = fd.read()
            fd.close()

            lines = wholeFile.split('\n')

            idx = 0
            while idx < len(lines):

                try:
                    while not re.search(SEQUENCE_PATTERN, lines[idx]):
                        idx += 1

                    descriptorCode = lines[idx][2] + lines[idx][4:6] + \
                                     lines[idx][7:10]
                    p = lines[idx].split('|')
                    p1 = p[1].split(';')
                    mnemonic = p1[0].strip()
                    self[descriptorCode] = TableDEntry(mnemonic)
                    idx += 1
                    while re.search(DESCRIPTOR_PATTERN, lines[idx]):
                        childCode = lines[idx][13] + \
                                    lines[idx][15:17] \
                                    + lines[idx][18:21]
                        self[descriptorCode].descriptors.append(
                            childCode)
                        idx += 1
                        if idx == len(lines):
                            break
                except IndexError:
                    #print("key to error: bad key is %s in line %d" % \
                        #(descriptorCode, idx))
                    #print("there were %d lines" % (len(lines),))
                    break

                idx += 1

        return 


    def extend_table(self, tableMessage, tableB):

        idx = 1
        idx += tableMessage[idx-1]*67

        idx += tableMessage[idx]*112 + 1

        idx += 1
        print "Are there really ", tableMessage[idx-1], " Table D Entries?"
        for i in range(tableMessage[idx-1]): 
            descriptorCode = tableMessage[idx:idx+6].tostring()
            mnemonic = tableMessage[idx+6:idx+15].tostring().split()[0]
            self[descriptorCode] = TableDEntry(mnemonic)
            idx += 6 + 64 + 1
            for j in range(tableMessage[idx-1]):
                childCode = tableMessage[idx:idx+6].tostring()
                self[descriptorCode].descriptors.append(childCode)
                #if childCode[0] == '0':
                    #self[descriptorCode].descriptors.append(tableB[childCode])
                #elif childCode[0] == '3':
                    #if childCode in self.keys():
                        #self[descriptorCode].descriptors.append(self[childCode])
                    #else:
                        #self[descriptorCode].descriptors.append(childCode)
                idx += 6

        #for k in self.keys():
            #for a in self[k].descriptors:
                #if isinstance(a, str):
                    #self[k].descriptors[self[k].descriptors.index(a)] \
                        #= self[a]

        return
