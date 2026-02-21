bl_info = {
    "name": "Wuwa Color & Texcoord",
    "author": "UNAMED666",
    "version": (1, 0, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Sidebar > Tool",
    "category": "Object",
}

import bpy

# ------------------------------------------------------
# UTIL
# ------------------------------------------------------

def log(self, msg):
    print(f"[Wuwa] {msg}")
    self.report({'INFO'}, msg)


def get_active_render_uv(mesh):
    for uv in mesh.uv_layers:
        if getattr(uv, "active_render", False):
            return uv
    return mesh.uv_layers.active

#------------------------------------------------------
# SET COLOR
#------------------------------------------------------

class WUWA_OT_set_color(bpy.types.Operator):
    bl_idname = "wuwa.set_color"
    bl_label = "Set COLOR"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            mesh = obj.data
            log(self, f"Processing COLOR: {obj.name}")

            existing = {c.name for c in mesh.color_attributes}
            required = ["COLOR", "COLOR1"]

            for name in required:
                if name not in existing:
                    attr = mesh.color_attributes.new(name=name, type='BYTE_COLOR', domain='CORNER')
                    color = (1.0, 0.5, 0.5, 0.3)
                    for i in range(len(attr.data)):
                        attr.data[i].color = color
                    log(self, f"Created missing {name} on {obj.name}")
                else:
                    log(self, f"Exists {name} on {obj.name}")

        return {'FINISHED'}

#------------------------------------------------------
# SET TEXCOORD
#------------------------------------------------------

class WUWA_OT_set_texcoord(bpy.types.Operator):
    bl_idname = "wuwa.set_texcoord"
    bl_label = "Set TEXCOORD.xy"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            mesh = obj.data
            log(self, f"Processing TEXCOORD: {obj.name}")

            base = None
            for uv in mesh.uv_layers:
                if uv.name == "TEXCOORD.xy":
                    base = uv
                    break

            if base is None:
                active = get_active_render_uv(mesh)
                if active is None:
                    log(self, f"FAILED {obj.name}: no base UV")
                    continue
                active.name = "TEXCOORD.xy"
                base = active
                log(self, f"Renamed active UV to TEXCOORD.xy")

            existing = {uv.name for uv in mesh.uv_layers}

            for name in ["TEXCOORD1.xy", "TEXCOORD2.xy"]:
                if name not in existing:
                    new = mesh.uv_layers.new(name=name)
                    for i in range(len(mesh.loops)):
                        new.data[i].uv = base.data[i].uv
                    log(self, f"Created missing {name} on {obj.name}")
                else:
                    log(self, f"Exists {name} on {obj.name}")

        return {'FINISHED'}

#------------------------------------------------------
# CHECK UV
#------------------------------------------------------

class WUWA_OT_check_uv(bpy.types.Operator):
    bl_idname = "wuwa.check_uv"
    bl_label = "Check UV Map"

    allowed = {"TEXCOORD.xy", "TEXCOORD1.xy", "TEXCOORD2.xy"}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            mesh = obj.data
            names = {uv.name for uv in mesh.uv_layers}

            if not names:
                log(self, f"{obj.name}: NO UV MAP")
                continue

            missing = self.allowed - names
            extra = names - self.allowed

            if not missing and not extra and len(names) == 3:
                log(self, f"{obj.name}: OK (exact TEXCOORD set)")
            else:
                if missing:
                    log(self, f"{obj.name}: Missing {', '.join(missing)}")
                if extra:
                    log(self, f"{obj.name}: Extra {', '.join(extra)}")

        return {'FINISHED'}

#------------------------------------------------------
# CHECK COLOR
#------------------------------------------------------

class WUWA_OT_check_color(bpy.types.Operator):
    bl_idname = "wuwa.check_color"
    bl_label = "Check COLOR"

    allowed = {"COLOR", "COLOR1"}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            mesh = obj.data
            names = {c.name for c in mesh.color_attributes}

            if not names:
                log(self, f"{obj.name}: NO COLOR ATTRIBUTE")
                continue

            missing = self.allowed - names
            extra = names - self.allowed

            if not missing and not extra and len(names) == 2:
                log(self, f"{obj.name}: OK (COLOR set correct)")
            else:
                if missing:
                    log(self, f"{obj.name}: Missing {', '.join(missing)}")
                if extra:
                    log(self, f"{obj.name}: Extra {', '.join(extra)}")

        return {'FINISHED'}

#------------------------------------------------------
# UI
#------------------------------------------------------

class WUWA_PT_panel(bpy.types.Panel):
    bl_label = "Wuwa Tools"
    bl_idname = "WUWA_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("wuwa.set_texcoord")
        layout.operator("wuwa.set_color")
        layout.separator()
        layout.operator("wuwa.check_uv")
        layout.operator("wuwa.check_color")

#------------------------------------------------------
# REGISTER
#------------------------------------------------------

classes = (
    WUWA_OT_set_color,
    WUWA_OT_set_texcoord,
    WUWA_OT_check_uv,
    WUWA_OT_check_color,
    WUWA_PT_panel,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
