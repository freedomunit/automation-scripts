# -*- coding: utf-8 -*-

import sys 
import numpy as np 
import matplotlib.pyplot as plt 
import datetime

def drawLinuxMonitorCharts(monitorFileDir='',startTime='',endTime='',outDir=''):
    if(not startTime or not endTime):
        startTime = datetime.datetime.strptime("11:15:44 AM",'%H:%M:%S %p')
        endTime = datetime.datetime.strptime("11:16:50 AM",'%H:%M:%S %p')
    else:
        startTime = datetime.datetime.strptime(startTime,'%H:%M:%S %p')
        endTime = datetime.datetime.strptime(startTime,'%H:%M:%S %p')
    if(not monitorFileDir):
        monitorFileDir = 'D:\\temp\\load20170120_'
    if (not outDir):
        outDir = 'D:\\temp\\monitorCharts\\'
    drawCPUChart(monitorFileDir+"cpu.txt",startTime,endTime,outDir)
    drawMemoryChart(monitorFileDir+"memory.txt",startTime,endTime,outDir)
    drawQueueChart(monitorFileDir+"queue.txt",startTime,endTime,outDir)
    drawIOChart(monitorFileDir+"IO.txt",startTime,endTime,outDir)
    drawNetworkChart(monitorFileDir+"network.txt",startTime,endTime,outDir)

def drawCPUChart(filePath,startTime,endTime,outDir=''):
#    reload(sys)
#    sys.setdefaultencoding('utf-8')
#    startT = datetime.datetime.strptime(startTime,'%H:%M:%S %p')
#    endT = datetime.datetime.strptime(endTime,'%H:%M:%S %p')
    with open(filePath,'r') as cpuFile:
        cpuInfo= cpuFile.readlines()
    cpuList=[t.replace("\n","").split(" ") for t in cpuInfo[2:-1]]
    for m in range (0,len(cpuList)):
        n=0
        while (n< len(cpuList[m])):
            if(cpuList[m][n]==''):
                del cpuList[m][n]
            else:
                n+=1
    cpuCol = zip(*cpuList)
    userColIndex = [a for a,b in enumerate(cpuCol) if '%user' in b][0]
    sysColIndex = [a for a,b in enumerate(cpuCol) if '%system' in b][0]
    startRowIndex = [ a for a,b in enumerate(cpuCol[0]) for c,d in enumerate(cpuCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') >= startTime][0]
    endRowIndex = [ a for a,b in enumerate(cpuCol[0]) for c,d in enumerate(cpuCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') <= endTime][-1]
    x= [datetime.datetime.strptime(a+" "+b,'%H:%M:%S %p') for a,b in zip(cpuCol[0][startRowIndex:endRowIndex],cpuCol[1][startRowIndex:endRowIndex])]
    y=[float(c)+float(d) for c,d in zip(cpuCol[userColIndex][startRowIndex:endRowIndex],cpuCol[sysColIndex][startRowIndex:endRowIndex])]
#    print x
#    print y
    plt.figure()
    plt.plot(x,y)
    plt.ylim(0.00,100.00)
#    plt.xlim(startTime,endTime)
    plt.xlabel("time(s)")
    plt.ylabel("used(%)")
    plt.title("CPU Used%")
    plt.legend()
    plt.savefig(outDir+"cpu_used.png")

def drawMemoryChart(filePath,startTime,endTime,outDir=''):
#    reload(sys)
#    sys.setdefaultencoding('utf-8')
#    startT = datetime.datetime.strptime(startTime,'%H:%M:%S %p')
#    endT = datetime.datetime.strptime(endTime,'%H:%M:%S %p')
    with open(filePath,'r') as memFile:
        memInfo= memFile.readlines()
    memList=[t.replace("\n","").split(" ") for t in memInfo[2:-1]]
    for m in range (0,len(memList)):
        n=0
        while (n< len(memList[m])):
            if(memList[m][n]==''):
                del memList[m][n]
            else:
                n+=1
    memCol = zip(*memList)
    usedColIndex = [ a for a,b in enumerate(memCol) if '%memused' in b][0]
    startRowIndex = [ a for a,b in enumerate(memCol[0]) for c,d in enumerate(memCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') >= startTime][0]
    endRowIndex = [ a for a,b in enumerate(memCol[0]) for c,d in enumerate(memCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') <= endTime][-1]
    x= [datetime.datetime.strptime(a+" "+b,'%H:%M:%S %p') for a,b in zip(memCol[0][startRowIndex:endRowIndex],memCol[1][startRowIndex:endRowIndex])]
    y=[float(c) for c in memCol[usedColIndex][startRowIndex:endRowIndex]]
    plt.figure()
    plt.plot(x,y)
    plt.ylim(0.00,100.00)
#    plt.xlim(startTime,endTime)
    plt.xlabel("time(s)")
    plt.ylabel("used(%)")
    plt.title("Memory Used%")
    plt.legend()
    plt.savefig(outDir+"mem_used.png")

def drawQueueChart(filePath,startTime,endTime,outDir=''):
#    reload(sys)
#    sys.setdefaultencoding('utf-8')
#    startT = datetime.datetime.strptime(startTime,'%H:%M:%S %p')
#    endT = datetime.datetime.strptime(endTime,'%H:%M:%S %p')
    with open(filePath,'r') as queFile:
        queInfo= queFile.readlines()
    queList=[t.replace("\n","").split(" ") for t in queInfo[2:-1]]
    for m in range (0,len(queList)):
        n=0
        while (n< len(queList[m])):
            if(queList[m][n]==''):
                del queList[m][n]
            else:
                n+=1
    queCol = zip(*queList)
    queColIndex = [ a for a,b in enumerate(queCol) if 'runq-sz' in b][0]
    startRowIndex = [ a for a,b in enumerate(queCol[0]) for c,d in enumerate(queCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') >= startTime][0]
    endRowIndex = [ a for a,b in enumerate(queCol[0]) for c,d in enumerate(queCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') <= endTime][-1]
    x= [datetime.datetime.strptime(a+" "+b,'%H:%M:%S %p') for a,b in zip(queCol[0][startRowIndex:endRowIndex],queCol[1][startRowIndex:endRowIndex])]
    y=[float(c) for c in queCol[queColIndex][startRowIndex:endRowIndex]]
    plt.figure()
    plt.plot(x,y)
#    plt.xlim(startTime,endTime)
    plt.xlabel("time(s)")
    plt.ylabel("queue()")
    plt.title("queue")
    plt.legend()
    plt.savefig(outDir+"queue.png")

def drawIOChart(filePath,startTime,endTime,outDir=''):
#    reload(sys)
#    sys.setdefaultencoding('utf-8')
#    startT = datetime.datetime.strptime(startTime,'%H:%M:%S %p')
#    endT = datetime.datetime.strptime(endTime,'%H:%M:%S %p')
    with open(filePath,'r') as IOFile:
        IOInfo= IOFile.readlines()
    IOList=[t.replace("\n","").split(" ") for t in IOInfo[2:-1]]
    for m in range (0,len(IOList)):
        n=0
        while (n< len(IOList[m])):
            if(IOList[m][n]==''):
                del IOList[m][n]
            else:
                n+=1
    IOCol = zip(*IOList)
    tpsColIndex = [ a for a,b in enumerate(IOCol) if 'tps' in b][0]
    rtpsColIndex = [ a for a,b in enumerate(IOCol) if 'rtps' in b][0]
    wtpsColIndex = [ a for a,b in enumerate(IOCol) if 'wtps' in b][0]
    startRowIndex = [ a for a,b in enumerate(IOCol[0]) for c,d in enumerate(IOCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') >= startTime][0]
    endRowIndex = [ a for a,b in enumerate(IOCol[0]) for c,d in enumerate(IOCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') <= endTime][-1]
    x= [datetime.datetime.strptime(a+" "+b,'%H:%M:%S %p') for a,b in zip(IOCol[0][startRowIndex:endRowIndex],IOCol[1][startRowIndex:endRowIndex])]
    tps=[float(c) for c in IOCol[tpsColIndex][startRowIndex:endRowIndex]]
    rtps=[float(c) for c in IOCol[rtpsColIndex][startRowIndex:endRowIndex]]
    wtps=[float(c) for c in IOCol[wtpsColIndex][startRowIndex:endRowIndex]]
    plt.figure()
#    ax1=plt.subplot(133)
#    ax2=plt.subplot(132)
#    ax3=plt.subplot(131)
#    plt.xlim(startTime,endTime)
#    plt.sca(ax1)
    ptps=plt.plot(x,tps,label='tps')
#    plt.sca(ax2)
    prtps=plt.plot(x,rtps,label='rtps')
#    plt.sca(ax3)
    pwtps=plt.plot(x,wtps,label='wtps')
    plt.xlabel("time(s)")
    plt.ylabel("tps()")
    plt.title("IO")
    plt.legend()
    plt.savefig(outDir+"IO.png")

def drawNetworkChart(filePath,startTime,endTime,outDir=''):
#    reload(sys)
#    sys.setdefaultencoding('utf-8')
#    startT = datetime.datetime.strptime(startTime,'%H:%M:%S %p')
#    endT = datetime.datetime.strptime(endTime,'%H:%M:%S %p')
    with open(filePath,'r') as netFile:
        netInfo= netFile.readlines()
    netList=[t.replace("\n","").split(" ") for t in netInfo[2:-1]]
    for m in range (0,len(netList)):
        n=0
        while (n< len(netList[m])):
            if(netList[m][n]==''):
                del netList[m][n]
            else:
                n+=1
    netList=[t for t in netList if t[2] != 'lo'][:-1]
    netCol = zip(*netList)
    tranColIndex = [ a for a,b in enumerate(netCol) if 'txkB/s' in b][0]
    receColIndex = [ a for a,b in enumerate(netCol) if 'rxkB/s' in b][0]
    startRowIndex = [ a for a,b in enumerate(netCol[0]) for c,d in enumerate(netCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') >= startTime][0]
    endRowIndex = [ a for a,b in enumerate(netCol[0]) for c,d in enumerate(netCol[1]) if a==c and datetime.datetime.strptime(b+" "+d,'%H:%M:%S %p') <= endTime][-1]
    x= [datetime.datetime.strptime(a+" "+b,'%H:%M:%S %p') for a,b in zip(netCol[0][startRowIndex:endRowIndex],netCol[1][startRowIndex:endRowIndex])]
    trans=[float(c) for c in netCol[tranColIndex][startRowIndex:endRowIndex]]
    rece=[float(c) for c in netCol[receColIndex][startRowIndex:endRowIndex]]
    plt.figure()
#   plt.xlim(startTime,endTime)
    ptps=plt.plot(x,trans,label='transfer')
    prtps=plt.plot(x,rece,label='receiver')
    plt.xlabel("time(s)")
    plt.ylabel("net(KB)")
    plt.title("net")
    plt.legend()
    plt.savefig(outDir+"network.png")