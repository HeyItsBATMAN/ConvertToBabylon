# Author: Kai Niebes
# Description: Blender script to automatically import
# an OBJ model and convert it and it's materials into
# a single BABYLON model with integrated textures
# Requirements:
# Blender - 2.80
# Blender BABYLON script - https://github.com/BabylonJS/BlenderExporter
# Blender scene file (included next to this file)
# Running:
# With Blender in PATH, run
# blender blend-convert.blend --background --python blender-convert.py -- INPUT

# SYS and OS to get startup arguments and split them after the last double dash ("--")
# BPY for blender scene instructions
import sys
import bpy
import os

ARGV = sys.argv[sys.argv.index("--") + 1:]

INNAME, INEXT = os.path.splitext(ARGV[0])

SCALE = 0.5

print(ARGV)

if INEXT == ".obj":
  print("Handling .obj")
  # Import object and mirror it on the Y axis
  bpy.ops.import_scene.obj(filepath=ARGV[0], use_edges=True, use_smooth_groups=False, split_mode='OFF')
  bpy.ops.transform.resize(value=(SCALE, SCALE, SCALE), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
elif INEXT == ".ply":
  print("Handling .ply")
  bpy.ops.import_mesh.ply(filepath=ARGV[0])
  bpy.ops.transform.resize(value=(SCALE, SCALE, SCALE), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

print("Imported!")

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
