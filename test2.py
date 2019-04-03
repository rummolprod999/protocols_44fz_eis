import shutil

path_xml = "/home/alex/PycharmProjects/protocols_44fz_eis/test.py"
filexml = "test.py"


def copy_new_file(f, path):
    file_ex = path + '/' + f
    file_target = f'./unic_protocol/{f}'
    shutil.copy(file_ex, file_target)


try:
    dir_xml = path_xml.replace(f"/{filexml}", "")
    copy_new_file(filexml, dir_xml)
except Exception as ex1:
    print(ex1)
