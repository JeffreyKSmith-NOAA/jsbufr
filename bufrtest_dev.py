#!/usr/bin/env python

import array
import re

import Message
import Section0
import Section1
import Section2
import Section3
import Section4
import Section5
import TableB
import TableD

bufrFile = open("../test2/xx001", 'r')
tableB = TableB.TableB("../test2/bufrtab.TableB_STD_0_35")
tableD = TableD.TableD("../test2/bufrtab.TableD_STD_0_35")
msgCount = 0
while True:
    msgCount += 1
    print
    print("at the top of ", msgCount)
    s0 = Section0.Section0(bufrFile)
    #print(s0)
    s1 = Section1.Section1(bufrFile, s0.edition_number)
    #print(s1)
    #if s1.year > 0 or s1.month > 0 or s1.day > 0:
        #break

    if s1.optional_section_flag:
        s2 = Section2.Section2(bufrFile, s0.edition_number)
    s3 = Section3.Section3(bufrFile, s0.edition_number)
    print(s3)
    s4 = Section4.Section4(bufrFile, s0.edition_number)
    s5 = Section5.Section5(bufrFile)

    if not (s1.year > 0 or s1.month > 0 or s1.day > 0):
        #break
        tableB.extend_table(s4.data_contents)
        ks = tableB.keys()
        ks.sort()
        #print ks
        tableD.extend_table(s4.data_contents, tableB)

    print(s5)
    #if (s0.message_length % 4) == 0:
        #bufrFile.seek(4 - (s0.message_length % 4), 1)
    try:
        junk = array.array('B')
        junk.fromfile(bufrFile, 20)
        try:
            idx = junk.index(66)
            bufrFile.seek(-20, 1)
            bufrFile.seek(idx, 1)
        except:
            print "junk is bunk"
            bufrFile.seek(-60, 1)
            bunk = array.array('B')
            bunk.fromfile(bufrFile, 80)
            #print(bunk)
    except EOFError:
        print "found EOF"
        break
    if msgCount >= 84:
        print "84 records"
        break
    if msgCount > 13:
        print("Message")
        m = Message.DataMessage(s3, s4)
        m.expand_message(s4, tableB, tableD)
        print(m)
        #print(m.fields)
        print(m.get_value())

for k in tableD.keys():
    break
    #print(k, tableD[k].mnemonic, tableD[k].descriptors)
    print k, tableD[k].mnemonic, ": ",
    for d in tableD[k].descriptors:
        if d[0] == '0':
            print tableB[d].mnemonic, " ",
        elif d[0] == '3':
            print tableD[d].mnemonic, " ",
    print
    print
bufrFile.close()

