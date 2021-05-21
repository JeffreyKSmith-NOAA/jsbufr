import array

import Descriptor

class DataEntity:

    def __init__(self, descriptorCode):

        self.descriptor = Descriptor.Descriptor(descriptorCode)

        return

class DataEntityLeaf(DataEntity):

    def __init__(self, descriptorCode, tableB):

        DataEntity.__init__(self, descriptorCode)

        ks = tableB.keys()
        self.mnemonic = tableB[descriptorCode].mnemonic
        self.nbits = tableB[descriptorCode].nbits
        self.scale = tableB[descriptorCode].scale
        self.offset = tableB[descriptorCode].offset
        self.units = tableB[descriptorCode].units
        self.value = None

        return

    def get_value(self, s4, bitPtr):

        if self.units == "CCITT IA5":
            if (bitPtr % 8) == 0:
                self.value \
                    = s4.data_contents[bitPtr/8:(bitPtr+self.nbits)/8] \
                        .tostring()
            else:
                iValues = array.array('B')
                for i in range(self.nbits/8):
                    for j in range(8):
                        if s4.data_content[bytePtr] & BIT_MAP[varBitPtr % 8]:
                            v = 2*iValues + 1
                        else:
                            v = 2*iValues
                    iValues.append(v)
                self.value = iValues.tostring()
                        
        else:
            self.value = 0
            bytePtr = bitPtr/8
            varBitPtr = bitPtr % 8
            for i in range(self.nbits):
                if s4.data_content[bytePtr] & BIT_MAP[varBitPtr % 8]:
                    self.value = 2*self.value + 1
                else:
                    self.value = 2*self.value
                barBitPtr += 1
                if varBitPtr == 8:
                    varBitPtr = 0
                    bytePtr += 1
            if self.units != "CODE TABLE":
                self.value = self.scale*self.value + self.offset

        newBitPtr = bitPtr + self.nbits

        return self.value, newBitPtr

    def __repr__(self):

        return("mnemonic = %s, number of bits = %d, scale is %f" \
               % (self.mnemonic, self.nbits, self.scale))


class DataEntitySeq(DataEntity):

    def __init__(self, descriptorCode, s4, tableB, tableD):

        DataEntity.__init__(self, descriptorCode)
        
        self.mnemonic = tableD[descriptorCode].mnemonic
        self.members = []
        for d in tableD[descriptorCode].descriptors:
            if d[0] == '0':
                self.members.append(DataEntityLeaf(d, tableB))
            elif d[0] == '3':
                self.members.append(DataEntitySeq(d, s4, tableB, tableD))

        self.value = []

        return

    def add_member(self, member):

        self.members.append(member)

        return

    def get_value(self, s4, bitPtr):

        for m in member:
            (mValue, newBitPtr) = m.get_value(bitPtr)
            self.value.append(mValue)
            bitPtr = newBitPtr

        return self.value, newBitPtr

    def __repr__(self):

        return "sequence %s has %d members " % \
            (self.mnemonic, len(self.members))

class DataEntityRep(DataEntity):

    def __init__(self, repDescriptorCode, descriptorList):

        DataEntity.__init__(self, repDescriptorCode)

        if self.descriptor.y == 0:
            self.members = descriptorList[1:self.descriptor.x+1]
            self.num_reps = None
            # Next field should contain the number of repetitons, so get
            #length of the field
            if descriptorList[0].y == 0:
                self.nbits_rep = 1
            elif descriptorList[0].y == 1:
                self.nbits_rep = 8
            elif descriptorList[0].y == 2:
                self.nbits_rep = 16
        else:
            self.members = descriptorList[:self.descriptor.x]
            self.num_reps = self.descriptor.y
            self.nbits_rep = 0

        return

    def set_num_reps(self, message, bitPtr):

        if not self.num_reps:
            self.num_reps = extractInteger(message, bitPtr, self.nrep_bits)

        newBitPtr = bitPtr + self.nrep_bits
        return newBitPtr

    def get_value(self, bitPtr):

        self.value = []
        for m in self.members:
            (mValue, newBitPtr) = m.get_value(bitPtr)
            self.value.append(mValue)
            bitPtr = newBitPtr

        return self.value, newBitPtr

    def __repr__(self):
        return repr(self.num_reps)
