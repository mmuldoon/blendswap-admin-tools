bl_info = {
    "name": "BSwap Admin Tools",
    "description": "A set of tools used to help admins review products on BlendSwap.com",
    "author": "Matthew Muldoon, Ryan Sweeney",
    "version": (0, 2),
    "blender": (2, 73, 0),
    "location": "View3D > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "3D View"}

import bpy
import os, sys
import subprocess

class AdminTools(bpy.types.Panel):
    """A Custom Panel in the Viewport Toolbar"""
    bl_label = "Admin Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category ="BSwap"

    def draw(self, context):
        wm = context.window_manager        
        layout = self.layout
        
        row = layout.row()
        row.operator("file.copy_missing_files", text="Copy Missing File names")
        #operator ClipBoardOperator will set the is_missing variable to True
        #when it does, the below wil display
        if wm.is_missing:
            row = layout.row()
            row.label(text="Files are Missing", icon='ERROR')
            
            for item in wm.missing_files.split('\n'):
                row = layout.row()
                row.label(text=item)
        else:
            row = layout.row()
            row.label(text=wm.missing_files, icon='INFO')

class ClipBoardOperator(bpy.types.Operator):
    """Execute copy to clipboard"""
    bl_idname = "file.copy_missing_files"
    bl_label = "Copy missing files to clipboard"
    
    
    def execute(self, context):        
        msg = copy_missing_files()
        wm = context.window_manager
        if msg != "":            
            #Pop a message of the first missing file in the string in top bar
            self.report({'INFO'}, "Missing Files detected:" + msg.split('\n')[0] )
            wm.is_missing = True
            wm.missing_files = msg
        else:
            wm.is_missing = False
            wm.missing_files = "<No files missing>"
        return {'FINISHED'}
                

def list_missing_images():
    return [bpy.path.abspath(img.filepath) for img in bpy.data.images 
            if (not os.path.exists(bpy.path.abspath(img.filepath)) 
                and (img.packed_file is None))
        ]

def copy_missing_files():
    copy_text = ""
    for s in list_missing_images():
        if s != '':
            copy_text = copy_text + s + "\n"
    
    proc = None
    if sys.platform == 'win32':
        proc = subprocess.Popen(args=['clip'], stdin=subprocess.PIPE) # Windows
    elif sys.platform == 'darwin':
        proc = subprocess.Popen(args=['pbcopy'], stdin=subprocess.PIPE) # MAC
    #you can add 'xclip' for linux systems if you want.
    if proc:
        proc.stdin.write(bytes(copy_text, 'UTF-8'))
        proc.stdin.close()
        
    return copy_text

# Registration

def register():
    bpy.utils.register_module(__name__)
    
    wm = bpy.types.WindowManager
    #String containing the list of files.
    wm.missing_files = bpy.props.StringProperty(
        name = "Missing Files",
        default = "<No files missing>"
    )
    #True or False prperty used to determine whether to display in Panel
    wm.is_missing = bpy.props.BoolProperty(
        name = "Missing?",
        default= False
    )

def unregister():
    bpy.utils.unregister_module(__name__)

    wm = bpy.types.WindowManager
    del wm.missing_files    
    del wm.is_missing
    
if __name__== "__main__":
	register()