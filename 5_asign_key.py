import os

def assign():
    keyPath = "/Users/xue/Documents/Research/InputGeneration/apkAnalysis/keys/"
    apk_signedPath = "/Users/xue/Documents/Research/InputGeneration/apkAnalysis/signed_apks/"
    rebuildApkPath = "/Users/xue/Documents/Research/InputGeneration/apkAnalysis/rebuild_apks/"
    apkNameList = []

    for line in open(
            "/Users/xue/Documents/Research/InputGeneration/apkAnalysis/origin_apks_part/apkList.txt").readlines():
        line = line.strip()
        apkNameList.append(line)
    print(len(apkNameList))

    files = os.listdir(apk_signedPath)

    i = 0
    for apk_name in apkNameList:
        key_file = keyPath + apk_name + ".keystore"
        assigned_file = apk_signedPath + apk_name + ".apk"
        rebuild_file = rebuildApkPath + apk_name + ".apk"
        print("assigned apk: " + str(i))
        if apk_name in files:
            print("%s exists!!!!" % apk_name)
        else:
            cmd = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -storepass 123456 -keystore %s -signedjar %s %s abc.keystore" % (
                key_file, assigned_file, rebuild_file)
            print(cmd)
            os.system(cmd)
            i += 1


if __name__ == "__main__":

    assign()



