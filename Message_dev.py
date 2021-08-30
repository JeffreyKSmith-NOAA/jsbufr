import DataEntity
import Section3
import Section4
import TableC

class Message:
    def __init__(self, s3, s4):

        self.s3 = s3
        self.s4 = s4

        self.fields = []

        return

    def expand_message(self, s4, tableB, tableD):

        nreps = 1
        bitIndex = 0
        d = 0
        #modifier = False
        while d < len(self.s3.descriptors):

            if self.s3.descriptors[d].f == 0:
                self.fields.append(DataEntity.DataEntityLeaf(
                    self.s3.descriptors[d].fxy_string(), tableB))
                #if modifier:
                    #TableC.apply_C(self.fields[-1], s3.descriptors[d-1])
                    #modifier = False
            elif self.s3.descriptors[d].f == 1:
                self.fields.append(DataEntity.DataEntityRep(
                    self.s3.descriptors[d].fxy_string(),
                    self.s3.descriptors[d+1:], s4, tableB, tableD))
                d += len(self.fields[-1].members)
            elif self.s3.descriptors[d].f == 2:
                self.fields.append(DataEntity.DataEntityLeaf(
                    self.s3.descriptors[d].fxy_string(), tableB))
                #modifier = True
                #self.fields.append(DataEntity.DataEntityLeaf(
            elif self.s3.descriptors[d].f == 3:
                self.fields.append(DataEntity.DataEntitySeq(
                    self.s3.descriptors[d].fxy_string(), self.s4, tableB,
                    tableD))
            d += 1

        return


class TableMessage(Message):

    def __init__(self, s3, s4):

        Message.__init__(self, s3, s4)

        return

    def augment_tables(self):

        idx = 1
        for i in range(self.s4.data_contents[idx-1]):
            aString = self.s4.data_contents[idx:idx+67].tostring()
            idx += 67

        idx += 1
        for i in range(self.s4.data_contents[idx-1]):
            bString = self.s4.data_contents[idx:idx+112].tostring()
            idx += 112

        idx += 1
        for i in range(self.s4.data_contents[idx-1]):
            dString = self.s4.data_contents[idx:idx+22].tostring()
            idx += 22

        return (tableA, tableB, tableC)

class DataMessage(Message):

    def __init__(self, s3, s4):

        Message.__init__(self, s3, s4)

        return

    def get_value(self):

        value = []
        bitPtr = 0
        for f in self.fields:
            v, bitPtr = f.get_value(self.s4, bitPtr)
            value.append(v)

        return value

#    def __repr__(self):
#        return repr(self.fields)
