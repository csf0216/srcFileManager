import os,re

srcDir = r'C:\Users\wangmin\work\Wifi\wpa_supplicant_8\SI'

pattFunc = re.compile('\)\n\{[\d \D]+?\n\}')
#pattEnter = re.compile('(\d+\.\d+)')
pattLeave = re.compile('\n\s+return')
pattLeavereturn = re.compile('LEAVE\(\);\s+?return.*;')

for root,dirs,files in os.walk(srcDir):
    for fil in files:
        if fil.endswith('.c'):
            fd = open(os.path.join(root,fil),'r+')
            srcCode = fd.read()
            fd.close()
            l = 0
            for match in re.finditer(pattFunc, srcCode):
                srcCode = srcCode[:match.start()+l+3]+'\n    ENTER();'+srcCode[match.start()+l+3:]
                l += len('\n    ENTER();')
                srcCode = srcCode[:match.end()+l-2]+'\n    LEAVE();'+srcCode[match.end()+l-2:]
                l += len('\n    LEAVE();')
            l = 0
            for match in re.finditer(pattLeave, srcCode):
                srcCode = srcCode[:match.start()+l]+match.group()[:-6]+'LEAVE();'+srcCode[match.start()+l:]
                l += len(match.group()[:-6]+'LEAVE();')
            l = 0
            for match in re.finditer(pattLeavereturn, srcCode):
                srcCode = srcCode[:match.start()+l]+'{'+srcCode[match.start()+l:]
                l += 1
                srcCode = srcCode[:match.end()+l]+'}'+srcCode[match.end()+l:]
                l += 1      
            fd = open(os.path.join(root,fil),'w+')
            fd.write(srcCode)
            fd.close()
        