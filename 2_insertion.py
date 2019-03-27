import errno
import os
import subprocess

CONST_PATTERN = "Landroid/widget/EditText;->addTextChangedListener(Landroid/text/TextWatcher;)V"
CONST_PATTERN_LOCAL = ".local"

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


def get_apps(apk_list_file_path):

    apk_name_list = []
    for line in open(apk_list_file_path).readlines():
        line = line.strip()
        apk_name_list.append(line)
    return apk_name_list


def get_inserted_decode_files(root_path, apk):

    decode_path = root_path + "/decoded_and_filter_apks/" + apk
    insertion_path = root_path + "/insertions/" + apk

    # search the inserted files in insertion path
    cmd = "grep -lr \"%s\" %s" % (CONST_PATTERN, decode_path)
    try:
        byte_output = subprocess.check_output(cmd, shell=True)
        result = str(byte_output, 'utf-8')

        # copy all the files to insertion
        cmd = "cp -a %s %s" % (decode_path, insertion_path)
        print(cmd)
        os.system(cmd)

        return result.rstrip().split("\n")
    except subprocess.CalledProcessError:
        # no copy, since no pattern has been found.
        return None


# scan each file with PATTERN and insert the code
def scan_and_insert(apk_list_file_path, root_path):
    apk_name_list = get_apps(apk_list_file_path)
    for apk_name in apk_name_list:
        print(apk_name)
        inserted_decode_files = get_inserted_decode_files(root_path, apk_name)
        if inserted_decode_files is not None:
            for decode_file_path in inserted_decode_files:
                if 'android/support' not in decode_file_path:
                    insertion_file_path = decode_file_path.replace("/decoded_and_filter_apks", "/insertions")
                    # scan_and_insert_file(insertion_file_path, decode_file_path)
                    insert_at_beginning(insertion_file_path, decode_file_path)
                    # insert_every_method(insertion_file_path, decode_file_path)


def scan_and_insert_file(insertion_file_path, decode_file_path):
    # TODO: check the insertion, seems to be duplicated written.
    #   Need to modify to apply the pattern that appears in multiple locations.
    pattern = "Landroid/widget/EditText;->addTextChangedListener(Landroid/text/TextWatcher;)V"
    pattern_local = ".locals"
    is_buffer = False
    method = ""
    method_name = ""
    method_head, method_local, method_body = "", "", ""

    with open(insertion_file_path, "w") as f_insertion_write:
        with open(decode_file_path, "r") as f_decode_read:
            for line in f_decode_read:
                # case 1: is in the middle of a method
                if is_buffer:
                    if is_method_end(line):  # case 1.1, meet endline of a method
                        method = method_head + method_local + method_body + inserted_text(line, method_name) + line
                        is_buffer = False
                        f_insertion_write.write(method)
                    else:  # case 1.2, in the body of a method
                        if pattern_local in line:  # case 1.2.1, find .local in method
                            method_local = line
                            continue
                        if pattern in line:  # case 1.2.2, find pattern in method
                            method_body = method_body + line
                            method_local = update_local(method_local) + "\n"
                            continue
                        else:  # case 1.2.3, others
                            method_body = method_body + line
                            continue
                else:  # case 2: is not in the middle of a method
                    if is_method_start(line):
                        method_name = get_method_name(line)
                        method_head = line
                        is_buffer = True
                    else:
                        f_insertion_write.write(line)

    f_insertion_write.close()
    f_decode_read.close()


def insert_at_beginning(insertion_file_path, decode_file_path):

    is_buffer = False
    method_name = ""
    method_head, method_local, method_body, method_end= "", "", "", ""
    added_part = ""

    with open(insertion_file_path, "w") as f_insertion_write:
        with open(decode_file_path, "r") as f_decode_read:
            for line in f_decode_read:
                # case 1: is in the middle of a method
                if is_buffer:
                    if is_method_end(line):  # case 1.1, meet endline of a methodß
                        is_buffer = False
                        method_end = line
                        f_insertion_write.write(method_head + method_local + added_part + method_body + method_end)
                    else:  # case 1.2, in the body of a method
                        if CONST_PATTERN_LOCAL in line:  # case 1.2.1, find .local in method
                            method_local = update_local(line)
                            continue
                        if CONST_PATTERN in line:  # if pattern detected, then insert code, otherwise, do not insert.
                            method_body = method_body + line
                            added_part = inserted_text_print_name(method_name, decode_file_path)
                            continue
                        else:  # case 1.2.1, others line, just directly append at method
                            method_body = method_body + line
                            continue
                else:  # case 2: is not in the middle of a method
                    if is_method_start(line):  # case 2.1: method start line, get method name to print
                        method_name = get_method_name(line)
                        method_head = line
                        is_buffer = True
                    else:
                        f_insertion_write.write(line)

    f_insertion_write.close()
    f_decode_read.close()


# def scan_and_insert_app(root_path):
#
#     decode_path = root_path + "/decoded_and_filter_apks"
#     insertion_path = root_path + "/insertions"
#
#     for (dirpath, dirnames, filenames) in os.walk(decode_path):
#         for file in filenames:
#             decode_file_path = os.path.abspath(dirpath + "/" + file)
#             insertion_file_path = decode_file_path.replace(decode_path, insertion_path)
#
#             # print(decode_path)
#             # print(insertion_path)
#             # print(decode_file_path)
#             # print(insertion_file_path)
#
#             # remove illegal symbols
#             # decode_file_path = decode_file_path.replace("$", "\$")
#             # insertion_file_path = insertion_file_path.replace("$", "\$")
#
#             # create a new file to insert, read from old decode file to make copy
#             if not os.path.exists(os.path.dirname(insertion_file_path)):
#                 try:
#                     os.makedirs(os.path.dirname(insertion_file_path))
#                 except OSError as exc:  # Guard against race condition
#                     if exc.errno != errno.EEXIST:
#                         raise
#
#             # when the file is not smali code, directly copy
#             if not decode_file_path.endswith(".smali"):
#                 cmd = "cp %s %s" % (decode_file_path, insertion_file_path)
#                 # print(cmd)
#                 os.system(cmd)
#                 continue
#
#             # ends with .smali
#             if decode_file_path.endswith(".smali"):
#                 if 'android/support' in decode_path:
#                     cmd = "cp %s %s" % (decode_file_path, insertion_file_path)
#                     # print(cmd)
#                     os.system(cmd)
#                     continue
#                 else:
#                     insert_every_method(insertion_file_path, decode_file_path)
#
#                 continue


def get_method_name(line):
    return line[len('.method '):line.find('(')]


def insert_every_method(insertion_file_path, decode_file_path):
    pattern_local = ".locals"
    is_buffer = False
    method_name = ""
    method_head, method_local, method_body = "", "", ""

    with open(insertion_file_path, "w") as f_insertion_write:
        with open(decode_file_path, "r") as f_decode_read:
            for line in f_decode_read:
                # case 1: is in the middle of a method
                if is_buffer:
                    if is_method_end(line):  # case 1.1, meet endline of a method
                        is_buffer = False
                        f_insertion_write.write(line)
                    else:  # case 1.2, in the body of a method
                        if pattern_local in line:  # case 1.2.1, find .local in method
                            method_local = update_local(line)
                            # method_added_part = inserted_text_method(method_name, decode_file_path, line.rstrip())
                            f_insertion_write.write(method_local + method_added_part)
                            continue
                        else:  # case 1.2.1, others line, just directly print out
                            f_insertion_write.write(line)
                            continue
                else:  # case 2: is not in the middle of a method
                    if is_method_start(line):  # case 2.1: method start line, get method name to print
                        method_name = get_method_name(line)
                        is_buffer = True
                        f_insertion_write.write(line)
                    else:
                        f_insertion_write.write(line)

    f_insertion_write.close()
    f_decode_read.close()


def update_local(old_local):
    # maximum register is v15, then local number will not exceed this amount
    pattern_local = ".locals "
    # get old number of local
    var_number = int(old_local[len(pattern_local) + old_local.find(pattern_local):])

    # update number of local
    if var_number < 12:
        var_new = str(var_number + 4)
    else:
        var_new = str(var_number)
        # do not update the var_new

    # var_new = str(var_number + 3)
    # var_new = str(var_number + 4)
    # var_new = str(var_number + 2)
    new_local = "    .locals " + var_new

    return new_local


def is_method_start(line):
    return line.startswith(".method")


def is_method_end(line):
    return line.startswith(".end method")


# insert text after certain pattern
def inserted_text(line):
    print(line)
    var = line[line.find("{") + 1:line.find("{") + 2]
    var_number: int = int(line[line.find("{") + 2:line.find(",")])  # find variable name number of EditText
    var_tag = "v" + str(var_number + 10)
    var_tmp_id = "v" + str(var_number + 11)
    var_log_id = "v" + str(var_number + 12)

    text_to_be_added = "\n\
    const-string " + var_tag + ", \"Xue: print EditText Id: \" \n\
    invoke-virtual{" + var + str(var_number) + "}, Landroid/widget/EditText;->getHint()Ljava/lang/CharSequence\n\
    move-result-object " + var_tmp_id + " \n\
    invoke-virtual{" + var_tmp_id + "}, Ljava/lang/String;->valueOf(I)Ljava/lang/String \n\
    move-result-object " + var_log_id + " \n\
    invoke-static{" + var_tag + ", " + var_log_id + "}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I \n\n"

    "Landroid/widget/EditText;->getHint()Ljava/lang/CharSequence;"
    return text_to_be_added


# insert text after certain pattern
def inserted_text(line, method_name):

    text_to_be_added = "\n\
    const-string v14, \"Xue: print Method Name: \" \n\
    const-string v15, \"%s\"\n\
    invoke-static{v14, v15}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I \n" %(method_name)

    return text_to_be_added


# insert method name and file path in each method.
def inserted_text_print_name(method_name, decode_file_path):

    # var_number: int = int(line[len('.locals ') + line.find('.locals'):])  # find variable name number of EditText
    # var_name_tag = "v" + str(var_number + 1)
    # var_path_tag = "v" + str(var_number + 2)
    # var_name = "v" + str(var_number + 3)
    # var_path = "v" + str(var_number + 4)

    text_to_be_added = "\n\
    const-string v1, \"Xue: print Method Name: \" \n\
    const-string v2, \"Xue: print Method Path: \" \n\
    const-string v3, \" %s \"\n\
    const-string v4, \" %s \" \n\
    invoke-static{v1, v3}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I \n\
    invoke-static{v2, v4}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I \n" % (method_name, decode_file_path)

    return text_to_be_added


if __name__ == "__main__":

    root_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis'
    apk_list_file_path = "/Users/xue/Documents/Research/InputGeneration/apkAnalysis/origin_apks_part/apkList.txt"

    scan_and_insert(apk_list_file_path, root_path)
