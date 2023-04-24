import bpy

bl_info = {
    "name": "Remove Empty Groups",
    "author": "Gary Carse",
    "version": (1, 0),
    "blender": (3, 40, 1),
    "location": "View3D > Object > Remove Empty Groups",
    "description": "Removes unused Vertex Groups from an object",
    "warning": "",
    "doc_url": "",
    "category": "Rigging",
}

#This is the operator and where you type the functions
def my_operator():
    #1. MAKE A GROUP LIST FOR average_weight
    def make_group_list():
        obj = []
        temp_list = []
        group_list = []
        so = bpy.context.selected_objects
        for i in so:
            obj.append(i)
            for i in obj:
                #I've used .extend here (with square brackets) to add every item to the list
                temp_list.extend([group[0] for group in i.vertex_groups.items()])
                for group_name in temp_list:
                    if group_name not in group_list:
                        group_list.append(group_name)
        return group_list


    #2. CHECK THE AVERAGE WEIGHT OF EACH VERTEX POINT
    def average_weight(vertex_group_names, obj):
        mesh = obj.data
        for vertex in mesh.vertices:
            for group in vertex.groups:
                if group.group in vertex_group_names and group.weight > 0.1:
                    return False
        return True
                
             
    #3. DELETE THE GROUP
    def delete_group(obj, vertex_group):
        obj.vertex_groups.remove(vertex_group)
        
    # GROUP_LIST DEFINED
    group_list = make_group_list()

    #4. MAIN FOR LOOP
    for obj in bpy.context.selected_objects: 
        for vertex_group_name in group_list:
            vertex_group = obj.vertex_groups.get(vertex_group_name)
            if vertex_group is not None:
                if average_weight([vertex_group.index], obj):
                    delete_group(obj,vertex_group)
        

#This is the class, where you define the button
class RemoveEmptyGroupsOperator(bpy.types.Operator):
    bl_idname = "object.remove_empty_groups_operator"
    bl_label = "Remove Empty Groups"

#This just says, when the button defined above is clicked, it'll run the code
    def execute(self, context):
        my_operator()
        return {'FINISHED'}

#This add the button to the menu
def add_to_vertex_group_specials_menu(self, context):
    self.layout.operator("object.remove_empty_groups_operator")

#Add the operator to the vertex group specials menu
bpy.types.MESH_MT_vertex_group_context_menu.append(add_to_vertex_group_specials_menu)


#This registers the entire thing
def register():
    bpy.utils.register_class(RemoveEmptyGroupsOperator)


def unregister():
    bpy.utils.unregister_class(RemoveEmptyGroupsOperator)


if __name__ == "__main__":
    register()

