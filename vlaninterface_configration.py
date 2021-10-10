# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 18:08:29 2021

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

def getvlandict(filetextblockline):
    vlaninterfaceblockline = list()
    revlanif = r'^interface (Vlan-interface(\d+))'
    revi = re.compile(revlanif)
    for n in filetextblockline:
        if len(n) > 0:
            if revi.match(n[0]) != None:
                vlaninterfaceblockline.append(copy.deepcopy(n))
            else:
                pass
        else:
            pass
    '''
    linelong = 0
    for v in vlaninterfaceblockline:
        if len(v) > linelong:
            linelong = len(v)
            print(linelong, end = '')
            print(v)
        else:
            pass
    '''

    redescrip = r'(description)'
    rede = re.compile(redescrip)
    reipaddress = r'(^ip address)'
    reip = re.compile(reipaddress)
    reippbr = r'(ip policy-based-route)'
    reipr = re.compile(reippbr)
    reipadd = r'(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)'
    reipd = re.compile(reipadd)

    vlaninterfacedictlist = list()
    vlaninterfaceindexlist = list()
    for vi in vlaninterfaceblockline:
        tempviflist = list()
        tempvifattlist = list()
        for n in vi:
            e = n.strip(' ')
            if revi.search(e) != None:
                tempvifm = revi.search(e)
                tempvifname = tempvifm.groups()[0]
                tempviflist.append(tempvifname)
                vlaninterfaceindexlist.append(tempvifname)
                vlannumber = tempvifm.groups()[1]
                vlanid = 'vlan' + ' ' +  vlannumber
                tempvifattlist.append(tuple(['vlanid',vlanid]))
            if rede.search(e) != None:
                tempdem = rede.search(e)
                tempdename = tempdem.groups()[0]
                tempdeatt = e[tempdem.span()[1]:].strip(' ')
                tempvifattlist.append(tuple([tempdename,tempdeatt]))
            if reip.search(e) != None:
                tempipm = reip.search(e)
                tempipname = tempipm.groups()[0]
                tempipatt = e[tempipm.span()[1]:].strip(' ')
                if reipd.search(e) != None:
                    ipdinfo = tempipatt.split(' ')
                    #print(vi)
                    #print(ipdinfo)
                    ipsubnet = str(IPy.IP(ipdinfo[0]).make_net(ipdinfo[1]))
                    tempvifattlist.append(tuple([tempipname,ipdinfo[0]]))
                    tempvifattlist.append(tuple(['ip mask',ipdinfo[1]]))
                    tempvifattlist.append(tuple(['ip subnet',ipsubnet]))
                    if len(ipdinfo) > 2:
                        tempvifattlist.append(tuple(['subinterface',ipdinfo[2]]))
                    else:
                        tempvifattlist.append(tuple(['subinterface','']))
                else:
                    tempvifattlist.append(tuple([tempipname,tempipatt]))
            if reipr.search(e) != None:
                tempiprm = reipr.search(e)
                tempiprname = tempiprm.groups()[0]
                tempipratt = e[tempiprm.span()[1]:].strip(' ')
                tempvifattlist.append(tuple([tempiprname,tempipratt]))
        tempviflist.append(dict(tempvifattlist))
        vlaninterfacedictlist.append(tuple(tempviflist))
    vlaninterfacedictlist.append(tuple(['vlaninterface',vlaninterfaceindexlist]))
    vlaninterfacedict = dict(vlaninterfacedictlist)
    return vlaninterfacedict











if __name__ == '__main__':
    configpath = r'E:\20210907_河西政务网网络设备配置信息'
    anaylispath = r'E:\20210914_河西政务网网络分析'
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d_%H-%M-%S')
    filename = r'vlaninterface-configration' + '_' + time_str + '.csv'
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

    allvlainterfaceconfig = list()
    for f in fileslist:
        print(f)
        templist = list()
        tempdict = dict()
        ftxt = makefiletext(f)
        ftxtb = makefiletextblock(ftxt)
        dlocal,dtype = getfilelocalandtype(ftxt)
        vlanifd = getvlandict(ftxtb)
        #print(vlanifd)

        templist.append(tuple(['devicelocation',dlocal]))
        templist.append(tuple(['devicetype',dtype]))
        tempdict = dict(templist)
        tempdict.update(vlanifd)

        allvlainterfaceconfig.append(copy.deepcopy(tempdict))

    attset = set()
    for f in allvlainterfaceconfig:
        for i in f['vlaninterface']:
            for att in list(f[i].keys()):
                attset.add(att)
    print(attset)

    csvline = list()
    csvheadlist = ['devicelocation','devicetype','vlaninterface']
    attlist = list(attset)
    attlist.sort()
    for att in attlist:
        csvheadlist.append(att)
    csvhead = tuple(csvheadlist)
    print(csvhead)

    for vifd in allvlainterfaceconfig:
        vlaninterfacelist = vifd['vlaninterface']
        for vinterf in vlaninterfacelist:
            tempviflist = list()
            for v in csvheadlist:
                if vifd.get(v) != None and v != 'vlaninterface':
                    tempviflist.append(vifd[v])
                elif v == 'vlaninterface':
                        tempviflist.append(vinterf)
                elif vifd[vinterf].get(v) != None:
                        tempviflist.append(vifd[vinterf][v])
                else:
                    tempviflist.append('')
            csvline.append(tuple(tempviflist))
    
    #for line in csvline:
    #    print(line)
    
    filew = codecs.open(filefullname,'w','utf-8')
    wf = csv.writer(filew)
    wf.writerow(csvhead)
    for l in csvline:
        wf.writerow(l)
    filew.close()


    print("+-----------All of files in <{}> was scan, {} files. vlanInterface infomation is {}, write to file <{}>.-----------+".format(configpath,len(fileslist),len(csvline),filefullname))