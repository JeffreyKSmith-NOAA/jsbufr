import array

import Descriptor
from BUFRConstants import *

class DataEntity:

    def __init__(self, descriptorCode):

        if isinstance(descriptorCode, Descriptor.Descriptor):
            self.descriptor = descriptorCode
        else:
            self.descriptor = Descriptor.Descriptor(descriptorCode)

        return

class DataEntityLeaf(DataEntity):

    def __init__(self, descriptorCode, tableB):

        DataEntity.__init__(self, descriptorCode)

        if self.descriptor.fxy_string()[0] == '2':
            self.mnemonic = "ANON"
            self.nbits = 8*int(descriptorCode[3:])
            self.scale = 0
            self.offset = 0
            self.units = "CCITT IA5"
        else:
            self.mnemonic = tableB[descriptorCode].mnemonic
            self.nbits = tableB[descriptorCode].nbits
            self.scale = tableB[descriptorCode].scale
            self.offset = tableB[descriptorCode].offset
            self.units = tableB[descriptorCode].units
        
        self.value = None

        return

    def get_value(self, s4, bitPtr):

        if self.units == "CCITT IA5":
            # retrieving a text field, so field length is a multiple of 8 bits
            if (bitPtr % 8) == 0:
                # starting on a byte boundary
                self.value \
                    = s4.data_contents[bitPtr/8:(bitPtr+self.nbits)/8] \
                        .tostring()
            else:
                # starting (and ending) in the middle of a byte
                iValues = array.array('B')
                varBitPtr = bitPtr
                for i in range(self.nbits/8):
                    iValues.append(0)
                    for j in range(8):
                        bytePtr = varBitPtr/8
                        if s4.data_contents[bytePtr] & BIT_MASK[varBitPtr % 8]:
                            v = 2*iValues[i] + 1
                        else:
                            v = 2*iValues[i]
                        varBitPtr += 1
                    iValues.append(v)
                self.value = iValues.tostring()
                        
        else:
            self.value = 0
            bytePtr = bitPtr/8
            varBitPtr = bitPtr % 8
            for i in range(self.nbits):
                if s4.data_contents[bytePtr] & BIT_MASK[varBitPtr]:
                    self.value = 2*self.value + 1
                else:
                    self.value = 2*self.value
                varBitPtr += 1
                if varBitPtr == 8:
                    varBitPtr = 0
                    bytePtr += 1
            if self.units != "CODE TABLE" and self.scale != 0:
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
        modifier = False
        d = 0
        while d < len(tableD[descriptorCode].descriptors):
            if tableD[descriptorCode].descriptors[d][0] == '0':
                self.members.append(DataEntityLeaf(
                    tableD[descriptorCode].descriptors[d], tableB))
                #if modifier:
                    #TableC.apply_C(self.members[-1], d-1)
                    #modifier = False
            elif tableD[descriptorCode].descriptors[d][0] == '1':
                self.members.append(DataEntityRep(
                    tableD[descriptorCode].descriptors[d],
                    tableD[descriptorCode].descriptors[d+1:], s4, tableB,
                    tableD))
                d += len(self.members[-1].members)
            elif tableD[descriptorCode].descriptors[d][0] == '2':
                self.members.append(DataEntityLeaf(
                    tableD[descriptorCode].descriptors[d], tableB))
            elif tableD[descriptorCode].descriptors[d][0] == '3':
                self.members.append(DataEntitySeq(
                    tableD[descriptorCode].descriptors[d], s4, tableB, tableD))
            d += 1

        self.value = []

        print("Sequence: ", self.descriptor.fxy_string(), [x.descriptor.fxy_string() for x in self.members])
        return

    def add_member(self, member):

        self.members.append(member)

        return

    def get_value(self, s4, bitPtr):

        for m in self.members:
            (mValue, newBitPtr) = m.get_value(s4, bitPtr)
            self.value.append(mValue)
            bitPtr = newBitPtr

        return self.value, newBitPtr

    def __repr__(self):

        return "sequence %s has %d members " % \
            (self.mnemonic, len(self.members))

class DataEntityRep(DataEntity):

    def __init__(self, repDescriptorCode, descriptorList, s4, tableB, tableD):

        DataEntity.__init__(self, repDescriptorCode)

        self.members = []
        if self.descriptor.y == 0:
            # delayed repetion. number of repetitions in next field.
            #self.members = descriptorList[1:self.descriptor.x+1]
            for d in descriptorList[1:self.descriptor.x+1]:
                print("looking at ", d)
                if d.f == 0:
                    self.members.append(DataEntityLeaf(d, tableB))
                elif d.f == 1:
                    self.members.append(DataEntityRep(d, descriptorList, s4,
                                                      tableB, tableD))
                elif d.f == 3:
                    self.members.append(DataEntitySeq(d, s4, tableB, tableD))
                try:
                    print("Added ", self.members[-1])
                except:
                    print(d)
            self.num_reps = None
            # Next field should contain the number of repetitons, so get
            #length of the field
            #if descriptorList[0].y == 0:
            if descriptorList[0][3:] == "000":
                self.nbits_rep = 1
            #elif descriptorList[0].y == 1:
            elif descriptorList[0][3:] == "001":
                self.nbits_rep = 8
            #elif descriptorList[0].y == 2:
            elif descriptorList[0][3:] == "002":
                self.nbits_rep = 16
            print("REP ",self.nbits_rep, [x.descriptor for x in self.members])
        else:
            # non-delayed repetition
            #self.members = descriptorList[:self.descriptor.x]
            for d in descriptorList[1:self.descriptor.x]:
                if d.f == '0':
                    self.members.append(d, tableB)
                elif d.f == '1':
                    self.member.append(d, descriptorList, s4, tableB, tableD)
                elif d.f == '2':
                    self.member.append(d)
                elif d.f == '3':
                    self.member.append(d, s4, tableB, tableD)
            self.num_reps = self.descriptor.y
            self.nbits_rep = 0

        return

    def set_num_reps(self, message, bitPtr):

        if not self.num_reps:
            #self.num_reps = extractInteger(message, bitPtr, self.nrep_bits)
            self.num_reps = 0
            for i in range(self.nbits_rep):
                if message[(bitPtr + i)/8] & BIT_MASK[(bitPtr + i) % 8]:
                    self.num_reps = 2*self.num_reps + 1
                else:
                    self.num_reps = 2*self.num_reps

        newBitPtr = bitPtr + self.nbits_rep
        return newBitPtr

    def get_value(self, s4, bitPtr):

        bitPtr = bitPtr + self.set_num_reps(s4.data_contents, bitPtr)

        value = []
        for i in range(self.num_reps):
            for m in self.members:
                (mValue, newBitPtr) = m.get_value(s4, bitPtr)
                value.append(mValue)
                bitPtr = newBitPtr

        return value, newBitPtr

    def __repr__(self):
        return self.num_reps, [x.descriptor.fxy_string() for x in self.members]
