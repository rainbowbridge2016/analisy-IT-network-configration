# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 21:25:55 2021

@author: Rainbow
"""

import re
import copy
import codecs
import csv
import IPy
import os
import datetime


def makefiletext(filename):
    filedata = list()
    #file = codecs.open(filename,'r','utf-8')
    file = open(filename,'r')
    for line in file:
        filedata.append(line)
        #filedata.append(re.sub(r'\r\n','',line))
    file.close()
    
    #filetext = ''
    filetup = tuple(filedata)
    filetext = ''.join(filetup)
    return filetext

def makefiletextblock(filetext):
    
    filetextnospace = re.sub(r'^#\s*','#',filetext)
    filetextnon = re.sub(r'\n','|',filetextnospace)
    filetextblock = filetextnon.split(r'#')
    filetextblockline = list()
    for b in filetextblock:
        temp = b.split('|')
        if temp[0] == '':
            temp.pop(0)
        if temp[-1] == '':
            temp.pop(-1)
        filetextblockline.append(copy.deepcopy(temp))
    return filetextblockline

def getfilelocalandtype(filetext):
    prompt = r'<([\w|-]*)>'
    reprompt = re.compile(prompt)
    promptobj = reprompt.search(filetext)
    promptstr = promptobj.groups()[0]
    promptlist = promptstr.split('-')
    if len(promptlist) > 2:
        location = promptlist[0] + '-' + promptlist[1]
        devicetype = promptlist[2]
    else:
        location = promptlist[0]
        devicetype = promptlist[1]
    return location, devicetype

def getospfdict(filetextblockline):
    #print('-------------------In getospfdict funtion-------------------')
    #print(filetextblockline)
    ospfblock = list()
    reospf = r'^ospf'
    reo = re.compile(reospf)
    #reospfarea = r'^\s*(area)'
    reospfarea = r'^\s*(area\s*[\d|\.]*)'
    reoa = re.compile(reospfarea)
    reospfareanetwork = r'^\s*(network)'
    reoan = re.compile(reospfareanetwork)
    reospfareachange = r'^%*(area\s*[\d|\.]*)'
    reoac = re.compile(reospfareachange)
    for n in filetextblockline:
        if len(n) > 0:
            if reo.match(n[0]) != None:
                ospfblock.append(copy.deepcopy(n))
            else:
                pass
        else:
            pass
    #print(ospfblock)
    ospfblocksyb = list()
    for i in ospfblock:
        templist = list()
        for n in i:
            if reo.match(n) != None:
                templist.append(copy.deepcopy(n))
            elif reoa.search(n) != None:
                a = reoa.sub(r'#%\1%',n)
                templist.append(copy.deepcopy(a))
            elif reoan.search(n) != None:
                b = reoan.sub(r'||\1',n)
                templist.append(copy.deepcopy(b))
                #templist.append(copy.deepcopy(n))
        c = ''.join(templist)
        d = c.split('#')
        ospfblocksyb.append(copy.deepcopy(d))
    #print(ospfblocksyb)
    ospfdict = dict()
    tempdictlist = list()
    for o in ospfblocksyb:
        areanametemp = ['ospfarea',]
        areanumlisttemp = list()
        for i in o:
            #print('#----------ospf information,and add in dictlist---------------')
            if reo.search(i) != None:
                temp = (i.strip(' ')).split(' ')
                if len(temp) > 2:
                    tempdictlist.append(tuple(['ospfinstance',temp[0] + ' ' + temp[1]]))
                    tempdictlist.append(tuple(['ospfrouterid',temp[2] + ' ' + temp[3]]))
                else:
                    tempdictlist.append(tuple(['ospfinstance',temp[0] + ' ' + temp[1]]))
                    tempdictlist.append(tuple(['ospfrouterid','']))
            else:
                pass
            #print('#----------ospf area information, make dict and add in dictlist---------')
            if reoac.search(i) != None:
                arealinelist = (i.strip(' ').split('%'))
                areainfo = arealinelist[1]

                areainfolist = (areainfo.strip(' ')).split(' ')
                areanumber = areainfolist[1]
                areanumlisttemp.append(areanumber)

                areanetinfo = arealinelist[2]
                areanetlist = (areanetinfo.strip(' ')).split('||')
                areanetlist.pop(0)
                
                areanumtemp = list()
                areanetlisttemp = list()
                areanumtemp.append(areanumber)
                for n in areanetlist:
                    b = (n.strip(' ')).split(' ')
                    netm = b[2].split('.')
                    netmtemp = list()
                    for m in netm:
                        netmtemp.append(str(255 - int(m)))
                    c = str(IPy.IP(b[1]).make_net('.'.join(netmtemp)))
                    areanetlisttemp.append(c)
                areanumtemp.append(areanetlisttemp)
                tempdictlist.append(tuple(areanumtemp))
        areanametemp.append(areanumlisttemp)
        tempdictlist.append(tuple(areanametemp))
    #print(tempdictlist)
    ospfdict = dict(tempdictlist)
    #print(ospfdict)
    return ospfdict



if __name__ == '__main__':
    configpath = r'....pleas type youself file dirctory....'
    anaylispath =r'....pleas type youself file dirctory....'
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d_%H-%M-%S')
    filename = r'ospf-configuration' + '_' + time_str + '.csv'
    filefullname = anaylispath + '\\' + filename
    
    os.chdir(configpath)
    refiledotname = r'.txt$'
    refen = re.compile(refiledotname)
    dirfile = os.listdir()
    txtfilelist = list()
    for f in dirfile:
        if refen.search(f) != None:
            txtfilelist.append(f)
    
    fileslist = list()
    for f in txtfilelist:
        fileslist.append(configpath + '\\' + f)

    allospfconfig = list()
    for f in fileslist:
        print(f)
        templist = list()
        tempdict = dict()
        ftxt = makefiletext(f)
        ftxtb = makefiletextblock(ftxt)
        dlocal,dtype = getfilelocalandtype(ftxt)
        ospfd = getospfdict(ftxtb)

        templist.append(tuple(['devicelocation',dlocal]))
        templist.append(tuple(['devicetype',dtype]))
        tempdict = dict(templist)
        tempdict.update(ospfd)
        allospfconfig.append(copy.deepcopy(tempdict))
    #for os in allospfconfig:
    #    print(os)
    
    csvline = list()
    csvhead = tuple(['devicelocation','devicetype','ospfinstance','ospfrouterid','ospfarea','subnetwork'])
    for o in allospfconfig:
        for a in o['ospfarea']:
            asubnet = o[a]
            for n in asubnet:
                tempospf = list()
                #print(n)
                tempospf.append(o['devicelocation'])
                tempospf.append(o['devicetype'])
                tempospf.append(o['ospfinstance'])
                tempospf.append(o['ospfrouterid'])
                tempospf.append(a)
                tempospf.append(n)
                csvline.append(tuple(tempospf))
    #print(csvline)

    filew = codecs.open(filefullname,'w','utf-8')
    wf = csv.writer(filew)
    wf.writerow(csvhead)
    for l in csvline:
        wf.writerow(l)
    filew.close()

    print("+-----------All of files in <{}> was scan, {} files. Ospf routes infomation is {}, write to file <{}>.-----------+".format(configpath,len(fileslist),len(csvline),filefullname))
