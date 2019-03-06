import os


def create_apk_list(apk_path, apk_list):
    arr_apk = [x for x in os.listdir(apk_path) if x.endswith(".apk")]
    # write to apklist
    f = open(apk_list,"w+")
    for apk in arr_apk:
        file_name = apk.replace(".apk", "")
        f.write("%s\n" % file_name)
    f.close()


def decode(apk_path, decode_path, name_list):
    with open(name_list) as f:
        for line in f:
            if os.path.exists((decode_path+line).rstrip()):
                print(line + " exists!!")
                continue
            else:
                cmd = "apktool d %s%s.apk -o %s%s" % (apk_path, line.rstrip(), decode_path, line.rstrip())
                print(cmd)
                os.system(cmd)


if __name__ == "__main__":

    apk_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis/origin_apks_can_rebuild/'
    decode_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis/decoded_apks/'
    apk_list = apk_path + "apkList.txt"
    #print("com.tabtale.catsdressup.apk".replace(".apk", ""))
    create_apk_list(apk_path, apk_list)
    decode(apk_path, decode_path, apk_list)