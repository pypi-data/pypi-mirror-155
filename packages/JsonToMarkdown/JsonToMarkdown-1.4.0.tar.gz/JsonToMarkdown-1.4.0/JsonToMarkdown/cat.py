import os
import re
import sys

def cat_md(out_dir, file_msg):
    out_dir = out_dir
    doc_dir = os.path.join(out_dir, '_json_output', file_msg)
    for i in os.listdir(out_dir):
        path = os.path.join(out_dir, i)
        if os.path.isdir(path):
            continue
        if i == "list.md":
            continue
        reg_name = re.sub('\(.*\)', '', i[7:])
        reg_file = os.path.join(doc_dir, reg_name)
        if not os.path.exists(reg_file):
            print(path)
    
        cmd = 'cat "' + path + '" >> "' + reg_file + '"'
        os.system(cmd)
