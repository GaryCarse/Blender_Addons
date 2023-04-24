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


# DELETE A VERTEX GROUP FROM AN OBJECT 
# IF ALL THE VERTEX WEIGHTS OF THE GROUP ARE LESS THAN A GIVEN THRESHOLD
def delete_unused_vertex_groups(weight_threshold=0.1):
    # 1. MAKE A GROUP LIST FOR average_weight
    def make_group_list():
        obj = []
        temp_list = []
        group_list = []
        so = bpy.context.selected_objects
        for i in so:
            obj.append(i)
            for i in obj:
                # I've used .extend here (with square brackets) to add every item to the list
                temp_list.extend([group[0] for group in i.vertex_groups.items()])
                for group_name in temp_list:
                    if group_name not in group_list:
                        group_list.append(group_name)
        return group_list

    # 2. CHECK THE AVERAGE WEIGHT OF EACH VERTEX POINT
    def average_weight(vertex_group_names, obj):
        mesh = obj.data
        for vertex in mesh.vertices:
            for group in vertex.groups:
                if group.group in vertex_group_names and group.weight > weight_threshold:
                    return False
        return True

    # 3. DELETE THE GROUP
    def delete_group(obj, vertex_group):
        obj.vertex_groups.remove(vertex_group)

    # GROUP_LIST DEFINED
    group_list = make_group_list()

    # MAIN FOR LOOP
    for obj in bpy.context.selected_objects:
        for vertex_group_name in group_list:
            vertex_group = obj.vertex_groups.get(vertex_group_name)
            if vertex_group is not None:
                if average_weight([vertex_group.index], obj):
                    delete_group(obj, vertex_group)


class RemoveUnusedVertexGroupsOperator(bpy.types.Operator):
    """Remove unused vertex groups"""
    bl_idname = "object.remove_unused_vertex_groups"
    bl_label = "Remove Unused Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    weight_threshold: bpy.props.FloatProperty(
        name="Weight Threshold",
        description="Vertex groups with total weight below this threshold will be removed",
        default=0.1,
        min=0.0,
        max=1.0,
        precision=3,
    )

    def execute(self, context):
        group_list = make_group_list()

        for obj in bpy.context.selected_objects:
            for vertex_group_name in group_list:
                vertex_group = obj.vertex_groups.get(vertex_group_name)
                if vertex_group is not None:
                    if average_weight([vertex_group.index], obj, self.weight_threshold):
                        delete_group(obj, vertex_group)

        return {'FINISHED'}



def register():
    bpy.utils.register_class(RemoveUnusedVertexGroupsOperator)


def unregister():
    bpy.utils.unregister_class(RemoveUnusedVertexGroupsOperator)


if __name__ == "__main__":
    register()
