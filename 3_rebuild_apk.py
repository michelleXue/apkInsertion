
import os


apkNameList = []


def rebuild_apk(rebuild_apk_path, decode_file_path):
    i = 1
    for file in os.listdir(decode_file_path):
        print(i)
        if os.path.isfile(os.path.join(decode_file_path, file)):
            continue

        if file in os.listdir(rebuild_apk_path):
            print("Exists!!!!")

        else:
            # rebuild
            cmd = "apktool b %s%s -o %s%s.apk" % (decode_file_path, file, rebuild_apk_path, file)
            print(cmd)
            os.system(cmd)
        i += 1


if __name__ == "__main__":
    rebuild_apk_path = "/Users/xue/Documents/Research/InputGeneration/apkAnalysis/rebuild_apks/"
    decode_file_path = "/Users/xue/Documents/Research/InputGeneration/apkAnalysis/insertion/"
    rebuild_apk(rebuild_apk_path, decode_file_path)