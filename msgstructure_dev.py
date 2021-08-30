#!/usr/bin/env python

import array
import re
import sys

import Message
import Section0
import Section1
import Section2
import Section3
import Section4
import Section5
import TableB
import TableD

def msgstructure(bufrFilePath, msgType):

    bufrFile = open(bufrFilePath, 'r')
    #tableB = TableB.TableB("../test2/bufrtab.TableB_STD_0_35")
    #tableD = TableD.TableD("../test2/bufrtab.TableD_STD_0_35")
    tableB = TableB.TableB()
    tableD = TableD.TableD()

    msgCount = 0
    while True:
        msgCount += 1
        #print
        #print("at the top of ", msgCount)
        s0 = Section0.Section0(bufrFile)
        s1 = Section1.Section1(bufrFile, s0.edition_number)

        if s1.optional_section_flag:
            s2 = Section2.Section2(bufrFile, s0.edition_number)
        s3 = Section3.Section3(bufrFile, s0.edition_number)
        #print(s3)
        s4 = Section4.Section4(bufrFile, s0.edition_number)
        s5 = Section5.Section5(bufrFile)

        if s1.year == 0 and s1.month == 0 and s1.day == 0:
            tableB.extend_table(s4.data_contents)
            tableD.extend_table(s4.data_contents, tableB)

        try:
            junk = array.array('B')
            junk.fromfile(bufrFile, 20)
            try:
                idx = junk.index(66)
                bufrFile.seek(-20, 1)
                bufrFile.seek(idx, 1)
            except:
                bufrFile.seek(-60, 1)
                bunk = array.array('B')
                bunk.fromfile(bufrFile, 80)
        except EOFError:
            break


    bufrFile.close()

    for k in tableD.keys():
        if tableD[k].mnemonic == msgType:
            break
    printMsgStructure(k, tableD, tableB, "  ")

    return

def printMsgStructure(node, tableD, tableB, indentation):

    print indentation, tableD[node].mnemonic, ':'

    leaves = []
    for d in tableD[node].descriptors:
        if d[0] == '0':
            leaves.append(tableB[d].mnemonic)
        elif d[0] == '3':
            printMsgStructure(d, tableD, tableB, indentation + "  ")
    print indentation, "  ", " ".join(leaves)
  
    return
    
if __name__ == "__main__":
    msgstructure(sys.argv[1], sys.argv[2])
