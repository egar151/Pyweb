from fileinput import close
import os
from shutil import move
from tempfile import mkstemp


def replace('demo.dat', pattern, subst):
   file_path = os.path.abspath(file_path)
   #Create temp file
   fh, abs_path = mkstemp()
   new_file = open(abs_path,'w')
   old_file = open(file_path)
   for line in old_file:
        new_file.write(subst if pattern in line else line)
   #close temp file
   new_file.close()
   close(fh)
   old_file.close()
   #Remove original file
   os.remove(file_path)
   #Move new file
   move(abs_path, file_path)