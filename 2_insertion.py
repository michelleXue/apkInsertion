import fileinput
import os
import pathlib


class Apk:

    def __init__(self):
        self.name = ""
        self.path = ""
        self.input_num = 0
        self.has_search = False

    def __init__(self, name):
        self.name = name
        self.path = ""
        self.input_num = 0
        self.has_search = False

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def set_input_num(self, num):
        self.input_num = num

    def get_input_num(self):
        return self.input_num

    def set_search(self, result):
        self.has_search = result

    def has_search(self):
        return self.has_search


def scan_and_insert(files_path):
    pattern = "Landroid/widget/EditText;->addTextChangedListener(Landroid/text/TextWatcher;)V"
    prefix = "invoke-virtual {"
    for root, dirs, files in os.walk(files_path):
        for fname in files:
            path = os.path.join(root, fname)
            if fname.endswith(".smali"):
                print('analyzing ' + str(path) + '...')
                for line in fileinput.FileInput(path, inplace=1):
                    if pattern in line:
                        if prefix in line:
                            line = line.replace(line, line + inserted_text(line))
                            print(line, end='')


def inserted_text(line):
    var = line[line.find("{") + 1:line.find("{") + 2]
    var_number: int = int(line[line.find("{") + 2:line.find(",")])  # find variable name number of EditText
    var_tag = "v" + str(var_number + 10)
    var_tmp_id = "v" + str(var_number + 11)
    var_log_id = "v" + str(var_number + 12)

    text_to_be_added = "\n\
    const-string " + var_tag + ", \"Xue: print EditText Id: \" \n\
    invoke-virtual{" + var + str(var_number) + "}, Landroid /widget/EditText;->getHint()Ljava/lang/CharSequence;\n\
    move-result-object " + var_tmp_id + " \n\
    invoke-virtual{" + var_tmp_id + "}, Ljava/lang/String;->valueOf(I)Ljava/lang/String; \n\
    move-result-object " + var_log_id + " \n\
    invoke-static{" + var_tag + ", " + var_log_id + "}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I \n\n"

    return text_to_be_added


if __name__ == "__main__":

    files_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis/decoded_apks/'
    scan_and_insert(files_path)
