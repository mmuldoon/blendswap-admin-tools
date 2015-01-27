import bpy
import os
import subprocess

bpy.ops.file.report_missing_files()

def list_missing_images():
    return [bpy.path.abspath(img.filepath) for img in bpy.data.images if not os.path.exists(bpy.path.abspath(img.filepath))]

copy_text = ""
for s in list_missing_images():
    copy_text = copy_text + s + "\n"
    
#proc = subprocess.Popen(args=['clip'], stdin=subprocess.PIPE) # Windows
proc = subprocess.Popen(args=['pbcopy'], stdin=subprocess.PIPE) # MAC
proc.stdin.write(bytes(copy_text, 'UTF-8'))
proc.stdin.close()