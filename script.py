from fileinput import close
import os
from shutil import move
from tempfile import mkstemp

def find_replace(filename, find, replace):
    file_path = os.path.abspath(filename)
    fh ,abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(filename)
    for line in old_file:
        new_file.write(replace+'\n' if find in line else line)
    new_file.close()
    close()
    old_file.close()
    os.remove(file_path)
    move(abs_path, file_path)
