# Author: Kai Niebes
# Description: Blender script to automatically import
# an OBJ model and convert it and it's materials into
# a single BABYLON model with integrated textures
# Requirements:
# Blender - 2.79
# Blender BABYLON script - https://github.com/BabylonJS/Exporters/tree/master/Blender
# Blender scene file (included next to this file)
# Running:
# With Blender in PATH, run
# blender blend-convert.blend --background --python blender-convert.py -- INPUT OUTPUT

# SYS to get startup arguments and split them after the last double dash ("--")
# BPY for blender scene instructions
import sys
import bpy

ARGV = sys.argv[sys.argv.index("--") + 1:]

# Import object and mirror it on the Y axis
bpy.ops.import_scene.obj(filepath=ARGV[0], use_edges=True, use_smooth_groups=False, split_mode='OFF')
bpy.ops.transform.resize(value=(1, -1, 1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

# Sets Babylon Exporter to use inlineTextures
# This means and textures get included inside the BABYLON file
bpy.context.scene.inlineTextures = True

bpy.ops.export.bjs(filepath=ARGV[1])
