import os,re

logDir = r'C:\Users\wangmin\work\Study\wifiFramework\wpa_supplicant'

pattFunc = re.compile('\n\{[\d \D]+?\n\}')
#pattEnter = re.compile('(\d+\.\d+)')
pattLeave = re.compile('\n\s+return')
pattTime = re.compile('(\d+:\d+:\d+\.\d+)')

fd = open(logDir+r'\stalog','r+')
#fd = open(logDir+r'\p2plog','r+')
#fd = open(logDir+r'\hostapdlog','r+')

refinelog = ''

try:
    for line in fd.readlines():
        if 'wpa_supplicant:' in line:
            if 'Enter:' in line:
                pos = line.find('Enter:')
                refinelog += re.findall(pattTime, line)[0]+'    '+line[pos:]
            elif 'Leave:' in line:
                pos = line.find('Leave:')
                refinelog += re.findall(pattTime, line)[0]+'    '+line[pos:]
         
            else:
                pos = line.find('wpa_supplicant:')
                refinelog = refinelog[:-1]+' '+line[pos+16:-1]+refinelog[-1:]
finally:
    fd.close()

stack = 0
curPos = 0
traceBk = 50000
outlog = ''
for line in refinelog.split('\n'):
    print stack
    if 'Enter:' in line:
        l = line.find('Enter:')
        pos = curPos+l
        funcName = line[l+7:]
        outlog += line[:l]+'    '*stack+line[l:]+'\n'
        if pos+traceBk>len(refinelog):
            posEnd = len(refinelog)
        else:
            posEnd = pos+traceBk
        if 'Leave: '+funcName in refinelog[pos:posEnd]:
            stack += 1
        curPos += len(line)+1
    elif 'Leave:' in line:
        l = line.find('Leave:')
        pos = curPos+l
        funcName = line[l+7:]
        if pos-traceBk>0:
            posStart = pos-traceBk
        else:
            posStart = 0
        if 'Enter: '+funcName in refinelog[posStart:pos]:
            stack -= 1
        outlog += line[:l]+'    '*stack+line[l:]+'\n'
        curPos += len(line)+1
    
fd = open(logDir+r'\stalogxml','w+')
fd.write(outlog)
fd.close()

