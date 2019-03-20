import errno
import os


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


# def scan_and_insert(files_path):
#     pattern = "Landroid/widget/EditText;->addTextChangedListener(Landroid/text/TextWatcher;)V"
#     prefix = "invoke-virtual {"
#     for root, dirs, files in os.walk(files_path):
#         for fname in files:
#             path = os.path.join(root, fname)
#             if fname.endswith(".smali"):
#                 print('analyzing ' + str(path) + '...')
#                 for line in fileinput.FileInput(path, inplace=1):
#                     if pattern in line:
#                         if prefix in line:
#                             line = line.replace(line, line + inserted_text(line))
#                             print(line, end='')


# def scan_and_insert(files_path):
#     pattern = "Landroid/widget/EditText;->addTextChangedListener(Landroid/text/TextWatcher;)V"
#     pattern_local = ".locals"
#     prefix = "invoke-virtual {"
#
#     is_buffer = False
#     method_head, method_local, method_body, method_end = "", "", "", ""
#     method = ""
#
#     for root, dirs, files in os.walk(files_path):
#         for fname in files:
#             path = os.path.join(root, fname)
#             if fname.endswith(".smali"):
#                 print('analyzing ' + str(path) + '...')
#                 for line in fileinput.FileInput(path, inplace=1):
#                     # case 1: is in the middle of a method
#                     if is_buffer:
#                         if is_method_end(line):  # case 1.1, meet endline of a method
#                             method = method_head + method_local + method_body + line
#                             is_buffer = False
#                             print(method, end='')
#                         else:  # case 1.2, in the body of a method
#                             if pattern_local in line:  # case 1.2.1, find .local in method
#                                 method_local = line
#                                 continue
#                             if pattern in line:  # case 1.2.2, find pattern in method
#                                 method_body = method_body + line + inserted_text(line)
#                                 method_local = update_local(method_local) + "\n"
#                                 continue
#                             else:  # case 1.2.3, others
#                                 method_body = method_body + line
#                                 continue
#                     else:  # case 2: is not in the middle of a method
#                         if is_method_start(line):
#                             method_head = line
#                             is_buffer = True
#                         else:
#                             print(line, end='')
def scan_and_insert_app(root_path):

    decode_path = root_path + "/decoded_and_filtered"
    insertion_path = root_path + "/insertion"

    for (dirpath, dirnames, filenames) in os.walk(decode_path):
        for file in filenames:
            decode_file_path = os.path.abspath(dirpath + "/" + file)
            insertion_file_path = decode_file_path.replace(decode_path, insertion_path)

            # print(decode_path)
            # print(insertion_path)
            # print(decode_file_path)
            # print(insertion_file_path)

            # remove illegal symbols
            decode_file_path = decode_file_path.replace("$", "\$")
            insertion_file_path = insertion_file_path.replace("$", "\$")

            # create a new file to insert, read from old decode file to make copy
            if not os.path.exists(os.path.dirname(insertion_file_path)):
                try:
                    os.makedirs(os.path.dirname(insertion_file_path))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            # when the file is not smali code, directly copy
            if not decode_file_path.endswith(".txt"):
                cmd = "cp %s %s" % (decode_file_path, insertion_file_path)
                print(cmd)
                os.system(cmd)
                continue

            # ends with .smali
            if decode_file_path.endswith(".txt"):
                if 'android/support' in decode_path:
                    cmd = "cp %s %s" % (decode_file_path, insertion_file_path)
                    print(cmd)
                    os.system(cmd)
                    continue
                else:
                    scan_and_insert_file(insertion_file_path, decode_file_path)

                continue


def scan_and_insert_file(insertion_file_path, decode_file_path):

    pattern = "Landroid/widget/EditText;->addTextChangedListener(Landroid/text/TextWatcher;)V"
    pattern_local = ".locals"
    is_buffer = False
    method = ""
    method_head, method_local, method_body = "", "", ""

    with open(insertion_file_path, "w") as f_insertion_write:
        with open(decode_file_path, "r") as f_decode_read:
            for line in f_decode_read:
                # case 1: is in the middle of a method
                if is_buffer:
                    if is_method_end(line):  # case 1.1, meet endline of a method
                        method = method_head + method_local + method_body + line
                        is_buffer = False
                        f_insertion_write.write(method)
                    else:  # case 1.2, in the body of a method
                        if pattern_local in line:  # case 1.2.1, find .local in method
                            method_local = line
                            continue
                        if pattern in line:  # case 1.2.2, find pattern in method
                            method_body = method_body + line + inserted_text(line)
                            method_local = update_local(method_local) + "\n"
                            continue
                        else:  # case 1.2.3, others
                            method_body = method_body + line
                            continue
                else:  # case 2: is not in the middle of a method
                    if is_method_start(line):
                        method_head = line
                        is_buffer = True
                    else:
                        f_insertion_write.write(line)

    f_insertion_write.close()
    f_decode_read.close()


def update_local(old_local):
    pattern_local = ".locals"
    # get old number of local
    var_old =  old_local[old_local.find(pattern_local) + len(pattern_local) + 1]
    var_number = int(var_old)
    # update number of local
    var_new = str(var_number + 3)
    new_local = "    .locals " + var_new

    return new_local


def is_method_start(line):
    return line.startswith(".method")


def is_method_end(line):
    return line.startswith(".end method")


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

    root_path = '/Users/xue/Documents/Research/InputGeneration/apkAnalysis'

    scan_and_insert_app(root_path)
