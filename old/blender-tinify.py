# Author: Kai Niebes
# Description: Blender script to automatically import
# an OBJ or PLY model and convert it and it's
# materials/vertex colors into a single BABYLON model
# with integrated textures
# Requirements:
# Blender - 2.80
# Blender BABYLON script - https://github.com/BabylonJS/BlenderExporter
# Blender scene file (included next to this file)
# Running:
# With Blender in PATH, run
# blender blend-convert.blend --background --python blender-convert.py -- INPUT FACES SCALE

# SYS and OS to get startup arguments and split them after the last double dash ("--")
# BPY for blender scene instructions
import sys
import bpy
import os

ARGV = sys.argv[sys.argv.index("--") + 1:]

INNAME, INEXT = os.path.splitext(ARGV[0])

SUFFIXES = ["small", "medium", "large"]

SCALE = 0.5
if len(ARGV) > 2:
    SCALE = ARGV[2]

print("Input file ", ARGV[0])

if ARGV[1] == None:
    FACES = 200000
else:
    FACES = int(ARGV[1])

print("Reducing to: ")
print("Large:", 1.5*FACES)
print("Medium:", 1*FACES)
print("Small:", 0.5*FACES)

if INEXT == ".obj":
    # TODO: Bake OBJ Textures to vertex
    print("Handling .obj")
    bpy.ops.import_scene.obj(filepath=ARGV[0], use_edges=True, use_smooth_groups=False, split_mode='OFF')
    bpy.ops.transform.resize(value=(SCALE, SCALE, SCALE), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
elif INEXT == ".ply":
    print("Handling .ply")
    bpy.ops.import_mesh.ply(filepath=ARGV[0])
    bpy.data.objects[0].select_set(True)
    bpy.ops.transform.resize(value=(SCALE, SCALE, SCALE), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

# Export 3 quality settings
for x in range(3, 0, -1):
    # Deselect all
    for obj in bpy.data.objects:
        obj.select_set(False)

    # Decimate
    for obj in bpy.data.objects:
        obj.select_set(False)
        bpy.ops.object.modifier_add(type='DECIMATE')
        print("Decimating from ", len(bpy.context.object.data.polygons), "to", (FACES*(x*0.5)), "with a factor of", (FACES*(x*0.5))/len(bpy.context.object.data.polygons))
        bpy.context.object.modifiers["Decimate"].ratio = (FACES*(x*0.5))/len(bpy.context.object.data.polygons)
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")
        obj.select_set(False)

    # Select all
    for obj in bpy.data.objects:
        obj.select_set(True)
        # Remove Specular
        for slot in obj.material_slots:
            slot.material.specular_intensity = 0.0

    # Sets Babylon Exporter to use inlineTextures
    # This means and textures get included inside the BABYLON file
    bpy.context.scene.world.inlineTextures = True
    OUTNAME = INNAME + "_" + SUFFIXES[x-1] + ".babylon"

    print("Exporting to ", OUTNAME)

    bpy.ops.export.bjs(filepath=OUTNAME)
