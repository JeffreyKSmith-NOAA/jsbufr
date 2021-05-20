import array

import Descriptor

class DataEntity:

    def __init__(self, descriptor):

        self.descriptor = descriptor

        return

class DataEntityLeaf(DataEntity):

    def __init__(self, descriptor, tableB):

        DataEntity.__init__(self, descriptor)

        ks = tableB.keys()
        ks.sort()
        print(ks)
        self.mnemonic = tableB[descriptor].mnemonic
        self.nbits = tableB[descriptor].nbits
        self.scale = tableB[descriptor].scale
        self.offset = tableB[descriptor].offset
        self.units = tableB[descriptor].units
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

        return("first bit = %d, number of bits = %d, repetition is %d" \
               % (self.first_bit, self.nbits, self.repetition_index))


class DataEntitySeq(DataEntity):

    def __init__(self, descriptor, s4, tableB, tableD):

        DataEntity.__init__(self, descriptor)
        
        self.mnemonic = tableD[descriptor].mnemonic
        self.members = []
        for d in tableD[descriptor].descriptors:
            if d.f == 0:
                self.members.append(DataEntityLeaf(s4, tableB))
            elif d.f == 3:
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

        return "sequence has %d members with %d repetitiions " % (
            len(self.members), self.num_reps)

class DataEntityRep(DataEntity):

    def __init__(self, repDescriptor, descriptorList):

        DataEntity.__init__(self, repDescriptor)

        if self.descriptor.y == 0:
            self.members = descriptorList[1:self.descriptor.x+1]
            self.num_reps = None
            if descriptorList[0].y == 0:
                self.nbits_rep = 1
            elif descriptorList[0].y == 1:
                self.nbits_rep = 8
            elif descriptorList[0].y == 2:
                self.nbits_rep = 16
        else:
            self.members = descriptorList[:repDescriptor.x]
            self.num_reps = repDescriptor.y
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
