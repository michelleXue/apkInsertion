# This file is used to rule out the apk file that we do not analysis
import os


def filter_apk(input_path, output_path, apk_list):

    arr_apk = []

    # add complete path with apk file name to arr_apk
    with open(apk_list) as f:
        for line_terminated in f:
            line = line_terminated.rstrip('\n')
            arr_apk.append(line)

    # analyzing each folder, and keep the filtered apk in another list
    print('analyzing ' + str(apk_path) + '...')  # get each apk folder
    for apk_name in arr_apk:
        if has_pattern_in_apk(input_path + apk_name + "/"):
            # copy them to a new filtered folder.
            cmd = "cp -r %s %s" % ((input_path + apk_name + "/"), (output_path + apk_name + "/"))
            print(cmd)
            os.system(cmd)
        else:
            continue


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
    pattern = "Landroid/widget/EditText;->addTextChangedListener(Landroid/text/TextWatcher;)V"
    with open(path) as f:
        for line in f:
            if pattern in line:
                return True
            else:
                continue
    return False


if __name__ == "__main__":
    apk_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis/origin_apks/'
    decode_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis/decoded_apks/'
    filtered_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis/filtered_apks/'
    apk_list = apk_path + "apkList.txt"
    filter_apk(decode_path, filtered_path, apk_list)