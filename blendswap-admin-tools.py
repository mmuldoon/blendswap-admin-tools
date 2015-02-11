bl_info = {
    "name": "BSwap Admin Tools",
    "description": "A set of tools used to help admins review products on BlendSwap.com",
    "author": "Matthew Muldoon, Ryan Sweeney",
    "version": (0, 1),
    "blender": (2, 73, 0),
    "location": "View3D > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "3D View"}

import bpy
import os
import subprocess

class AdminTools(bpy.types.Panel):
	"""A Custom Panel in the Viewport Toolbar"""
	bl_label = "Admin Tools"
	bl_space_type = "VIEW_3D"

	bl_region_type = "TOOLS"
	bl_category ='BSwap'

	def draw(self, context):
		layout = self.layout
		
		row = layout.row()
		row.label(text="Test", icon='ERROR')


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



# Registration

def register():
	bpy.utils.register_class(AdminTools)

def unregister():
	bpy.utils.unregister_class(AdminTools)

if __name__== "__main__":
	register()
