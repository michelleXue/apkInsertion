import os


def decode(apk_path, decode_path, name_list):
    with open(name_list) as f:
        for line in f:
            if os.path.exists((decode_path+line).rstrip()):
                print(line + " exists!!")
                continue;
            else:
                cmd = "apktool d %s%s.apk -o %s%s" %(apk_path, line.rstrip(), decode_path, line.rstrip())
                print(cmd)
                os.system(cmd)


if __name__ == "__main__":

    apk_path = '/Users/xue/Documents/Research/InputGeneration/AppBrain_top_apps/apkAnalysis/test_apks/'
    decode_path = '/Users/xue/Documents/Research/InputGeneration/AppBrain_top_apps/apkAnalysis/test_decode/'
    apk_list = apk_path + "apkList.txt"
    decode(apk_path, decode_path, apk_list)