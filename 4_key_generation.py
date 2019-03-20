import subprocess
import pexpect
import sys
import os

keyPath = "/Users/xue/Documents/Research/InputGeneration/apkAnalysis/keys/"
apkNameList = []

for line in open(
        "/Users/xue/Documents/Research/InputGeneration/apkAnalysis/origin_apks_part/apkList.txt").readlines():
    line = line.strip()
    apkNameList.append(line)
print(len(apkNameList))

i = 0
files = os.listdir(keyPath)
for line in apkNameList:
    print("key assigned: " + str(i))
    line = line + ".keystore"
    if line in files:
        print("%s exists!!!!" % line)
    else:
        cmd1 = "keytool -genkeypair -dname \"cn=Mark Jones, ou=JavaSoft, o=Sun, c=US\" -alias business -keypass kpi135 -keystore %s -storepass ab987c -validity 20000" % (keyPath+line)
        print(cmd1)
        os.system(cmd1)
        # cmd2 = "keytool -importkeystore -srckeystore %s -destkeystore %s -deststoretype pkcs12" % (keyPath+line, keyPath+line)
        # print(cmd2)
        # os.system(cmd2)
        i += 1