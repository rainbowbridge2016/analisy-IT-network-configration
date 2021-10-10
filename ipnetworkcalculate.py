# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import codecs
import IPy

filer = open(r'....please type youself dot csv file....','r')
rf = csv.reader(filer)
recoder = list()
for i in rf:
    recoder.append(i)
filer.close()
title = recoder.pop(0)
title.append(r'IP网段')

location = recoder[0].index('ip address')
for r in recoder:
    q = str(IPy.IP(r[location+1]).make_net(r[location+2]))
    r.append(q)

filew = codecs.open(r'....please type youself dot csv file....','w','utf-8')
wf = csv.writer(filew)
wf.writerow(title)
for n in recoder:
    wf.writerow(n)
filew.close()