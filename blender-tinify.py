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
# blender blend-convert.blend --background --python blender-tinify.py -- INPUT

# SYS and OS to get startup arguments and split them after the last double dash ("--")
# BPY for blender scene instructions
import sys
import bpy
import os

ARGV = sys.argv[sys.argv.index("--") + 1:]

INNAME, INEXT = os.path.splitext(ARGV[0])

#print("Handling .obj")
#bpy.ops.import_scene.obj(filepath=ARGV[0], use_edges=True, use_smooth_groups=False, split_mode='OFF')
print("Handling .ply")
bpy.ops.import_mesh.ply(filepath=ARGV[0])
bpy.data.objects[0].select_set(True)

# Deselect all
for obj in bpy.data.objects:
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
OUTNAME = INNAME + ".babylon"

print("Exporting to ", OUTNAME)

bpy.ops.export.bjs(filepath=OUTNAME)
