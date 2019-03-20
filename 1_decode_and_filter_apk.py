import os

pattern = "Landroid/widget/EditText;->addTextChangedListener(Landroid/text/TextWatcher;)V"


def create_apk_list(apk_path, apk_list):
    arr_apk = [x for x in os.listdir(apk_path) if x.endswith(".apk")]
    # write to apklist
    f = open(apk_list,"w+")
    for apk in arr_apk:
        file_name = apk.replace(".apk", "")
        f.write("%s\n" % file_name)
    f.close()


def has_pattern_in_apk(apk_path):
    for root, dirs, files in os.walk(apk_path):
        for fname in files:
            path = os.path.join(root, fname)
            if fname.endswith(".smali"):
                if (has_pattern_in_line(path)):
                    return True
                else:
                    continue
            else:
                continue
    return False


def has_pattern_in_line(path):
    with open(path) as f:
        for line in f:
            if pattern in line:
                return True
            else:
                continue
    return False


def decode_and_filter(apk_path, decode_path, name_list):
    with open(name_list) as f:
        for line in f:
            if os.path.exists((decode_path+line).rstrip()):
                print(line + " exists!!")
                continue
            else:
                cmd = "apktool d %s%s.apk -o %s%s" % (apk_path, line.rstrip(), decode_path, line.rstrip())
                print(cmd)
                os.system(cmd)
                if(has_pattern_in_apk(decode_path + line.rstrip()+ "/")):
                    # do nothing
                    continue
                else:
                    # remove the decode apk file
                    print("No pattern exists!!!")
                    cmd = "rm -r %s%s" % (decode_path, line.rstrip())
                    print(cmd)
                    os.system(cmd)



if __name__ == "__main__":

    apk_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis/origin_apks_part/'
    decode_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis/decoded_and_filter_apks/'
    apk_list = apk_path + "apkList.txt"
    #print("com.tabtale.catsdressup.apk".replace(".apk", ""))
    # step 1: create an apklist for the original apks.
    create_apk_list(apk_path, apk_list)
    # step 2: decode and filter the apk folders
    decode_and_filter(apk_path, decode_path, apk_list)