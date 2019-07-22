# Converting very large 3D Models into small web-friendlier Babylon models using a combination of lossy techniques

# Requirements
- Meshlab
- Blender 2.80 (with Babylon Exporter)

# How it works
The python script meshlab-tinify.py takes a folder as an argument.

Starting from this folder, the script will search for .obj files.

For every .obj file, it will import this file into meshlab.

The imported mesh will be normalized using normalize.mlx

Afterwards, the mesh will be simplified and the texture will be transformed to vertex colors.

The mesh will be exported to 3 different .ply files.

Each of the .ply files will be imported to blender and exported as .babylon
using the blender-tinify.py script

