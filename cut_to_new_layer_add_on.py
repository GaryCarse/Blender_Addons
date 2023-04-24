import bpy

bl_info = {
    "name": "Cut Stroke To New Layer",
    "author": "Gary Carse",
    "version": (1, 0),
    "blender": (3, 50, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Cuts the stroke and pastes it onto a new layer",
    "category": "Grease Pencil",
}

#------------------------------------------------------

#MAIN OPERATOR

def cut_stroke():
    # Set the active object
    obj = bpy.context.active_object
    # Set the active GPencil data
    gp = obj.data
    # Get the active GPencil layer
    layer = gp.layers.active
    # Get the active GPencil frame
    frame = layer.active_frame

    #bpy.context.area.type = 'VIEW_3D'

    # Get the Stroke
    for points in frame.strokes:
        if points.select == True:
            bpy.ops.gpencil.copy()
            bpy.ops.gpencil.delete()
            
    # Create a new layer
    new_layer = gp.layers.new("New Layer")

    # Select the new layer
    gp.layers.active = new_layer

    # Add a new frame to the new layer
    new_frame = new_layer.frames.new(frame_number=frame.frame_number)

    bpy.ops.gpencil.paste()

    #bpy.context.area.ui_type = 'TEXT_EDITOR'
    
#----------------------------------------------------------
  
# THIS IS THE CLASS
class CutStrokeToNewLayer(bpy.types.Operator):
    """Cut Stroke To New Layer"""
    bl_idname = "editgpencil.cut_stroke_to_new_layer"
    bl_label = "Cut Stroke to New Layer"
    
    # THIS SAYS THE BUTTON WILL EXECUTE THE OPERATOR
    def execute(self, context):
        cut_stroke()
        return {'FINISHED'}


# This function adds the button to a menu (referenced in the below code)
def add_to_point_context_menu(self, context):
    self.layout.operator("editgpencil.cut_stroke_to_new_layer")
    
# This is the menu the button is being added to.
bpy.types.VIEW3D_MT_edit_gpencil_point.append(add_to_point_context_menu)

#This is the visual description of the menu button
def menu_draw(self, context):
    self.layout.operator("editgpencil.cut_stroke_to_new_layer", text = "Cut Stroke to New Layer")
    
#-------------------------------------------------------------------

def register():
    bpy.utils.register_class(CutStrokeToNewLayer)
    bpy.types.VIEW3D_MT_gpencil_edit_context_menu.append(menu_draw)

def unregister():
    bpy.utils.unregister_class(CutStrokeToNewLayer)
    bpy.types.VIEW3D_MT_gpencil_edit_context_menu.remove(menu_draw)

if __name__ == "__main__":
    register()
