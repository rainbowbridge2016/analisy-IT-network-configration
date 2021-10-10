# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 18:00:17 2021

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

def getinterfacedict(filetextblockline):
    interfaceblockline = list()
    reif = r'^interface\s([M|T|G|F][\w|-]*[/|\w]*)'
    rei = re.compile(reif)
    for n in filetextblockline:
        if len(n) > 0:
            if rei.match(n[0]) != None:
                interfaceblockline.append(copy.deepcopy(n))
            else:
                pass
        else:
            pass

    reiportmod = r'(port link-mode)'
    reipm = re.compile(reiportmod)
    reidescript = r'(description)'
    reid = re.compile(reidescript)
    reilinktype = r'(port link-type)'
    reilt = re.compile(reilinktype)
    #reiutrunkpermit = r'(undo port trunk permit)'
    #reiutp = re.compile(reiutrunkpermit)
    reitrunkpermit = r'(port trunk permit)'
    reitp = re.compile(reitrunkpermit)
    reilinkaggrega = r'(port link-aggregation)'
    reilag = re.compile(reilinkaggrega)
    reispeed = r'(speed)'
    reispd = re.compile(reispeed)
    reiipaddress = r'(ip address)'
    reiipd = re.compile(reiipaddress)
    #reiipnum = r'\d+\.\d+\.\d+\.\d+\s+\d+\.\d+\.\d+\.\d+'
    #reiipn = re.compile(reiipnum)
    reiipbind = r'(ip binding)'
    reiib = re.compile(reiipbind)
    reiportaccess = r'(port access)'
    reipa = re.compile(reiportaccess)

    #interfacedict = dict()
    interfacedictlist = list()
    interfaceindex = list()
    for i in interfaceblockline:
        tempiflist = list()
        tempifattributeslist = list()
        for n in i:
            e = n.strip(' ')
            if rei.search(e) != None: #r'^interface\s([M|T|G|F][\w|-]*[/|\w]*)'
                tempifname = rei.search(e).groups()[0]
                tempiflist.append(tempifname)
                interfaceindex.append(tempifname)
            if reipm.search(e) != None: # r'(port link-mode)'
                tempmipm = reipm.search(e)
                tempmodean = tempmipm.groups()[0].strip(' ')
                tempmodeatt = e[tempmipm.span()[1]:].strip(' ')
                tempifattributeslist.append(tuple([tempmodean,tempmodeatt]))
            if reid.search(e) != None: #r'(description)'
                tempmid = reid.search(e)
                tempidan = tempmid.groups()[0].strip(' ')
                tempidatt = e[tempmid.span()[1]:].strip(' ')
                tempifattributeslist.append(tuple([tempidan,tempidatt]))
            if reilt.search(e) != None: #r'(port link-type)'
                tempmilt = reilt.search(e)
                tempiltan = tempmilt.groups()[0].strip(' ')
                tempiltatt = e[tempmilt.span()[1]:].strip(' ')
                tempifattributeslist.append(tuple([tempiltan,tempiltatt]))
            if reipa.search(e) != None: #r'(port access)'
                tempmipa = reipa.search(e)
                tempipaan = tempmipa.groups()[0].strip(' ')
                tempipaatt = e[tempmipa.span()[1]:].strip(' ')
                tempifattributeslist.append(tuple([tempipaan,tempipaatt]))
            if reitp.search(e) != None: #r'(port trunk permit)'
                tempmitp = reitp.search(e)
                tempitpan = tempmitp.groups()[0].strip(' ')
                tempitpatt = e[tempmitp.span()[1]:].strip(' ')
                tempifattributeslist.append(tuple([tempitpan,tempitpatt]))
            if reilag.search(e) != None: #r'(port link-aggregation)'
                tempmilag = reilag.search(e)
                tempilagan = tempmilag.groups()[0].strip(' ')
                tempilagatt = e[tempmilag.span()[1]:].strip(' ')
                tempifattributeslist.append(tuple([tempitpan,tempitpatt]))
            if reiipd.search(e) != None: #r'(ip address)'
                tempmiipd = reiipd.search(e)
                tempipdan = tempmiipd.groups()[0].strip(' ')
                tempipdatt = e[tempmiipd.span()[1]:].strip(' ')
                ipdinfo = tempipdatt.split(' ')
                ipsubnet = str(IPy.IP(ipdinfo[0]).make_net(ipdinfo[1]))
                tempifattributeslist.append(tuple([tempipdan,ipdinfo[0]]))
                tempifattributeslist.append(tuple(['ip mask',ipdinfo[1]]))
                tempifattributeslist.append(tuple(['ip subnet',ipsubnet]))
        tempiflist.append(dict(tempifattributeslist))
        interfacedictlist.append(tuple(tempiflist))
    interfacedictlist.append(tuple(['interface',interfaceindex]))
    interfacedict = dict(interfacedictlist)
    return interfacedict







if __name__ == '__main__':
    configpath = r'....pleas type youself file dirctory....'
    anaylispath =r'....pleas type youself file dirctory....'
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d_%H-%M-%S')
    filename = r'interface-physic-port-configration' + '_' + time_str + '.csv'
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

    allinterfaceconfig = list()
    for f in fileslist:
        print(f)
        templist = list()
        tempdict = dict()
        ftxt = makefiletext(f)
        ftxtb = makefiletextblock(ftxt)
        dlocal,dtype = getfilelocalandtype(ftxt)
        interfaced = getinterfacedict(ftxtb)

        templist.append(tuple(['devicelocation',dlocal]))
        templist.append(tuple(['devicetype',dtype]))
        tempdict = dict(templist)
        tempdict.update(interfaced)

        allinterfaceconfig.append(copy.deepcopy(tempdict))
        #print(tempdict)

    attset = set()
    for f in allinterfaceconfig:
        for i in f['interface']:
            for att in list(f[i].keys()):
                attset.add(att)
    #print(attset)

    csvline = list()
    csvheadlist = ['devicelocation','devicetype','interface']
    attlist = list(attset)
    attlist.sort()
    for att in attlist:
        csvheadlist.append(att)
    csvhead = tuple(csvheadlist) 
    #print(csvhead)
    
    for ifd in allinterfaceconfig:
        interfacelist = ifd['interface']
        for interf in interfacelist:
            tempiflist = list()
            for v in csvheadlist:
                if ifd.get(v) != None and v != 'interface':
                    tempiflist.append(ifd[v])
                elif v == 'interface':
                        tempiflist.append(interf)
                elif ifd[interf].get(v) != None:
                        tempiflist.append(ifd[interf][v])
                else:
                    tempiflist.append('')
            csvline.append(tuple(tempiflist))
    
    #for line in csvline:
    #    print(line)
    filew = codecs.open(filefullname,'w','utf-8')
    wf = csv.writer(filew)
    wf.writerow(csvhead)
    for l in csvline:
        wf.writerow(l)
    filew.close()









    print("+-----------All of files in <{}> was scan, {} files. Interface physic port infomation is {}, write to file <{}>.-----------+".format(configpath,len(fileslist),len(csvline),filefullname))