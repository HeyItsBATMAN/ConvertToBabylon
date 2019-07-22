import sys
import os
from glob import glob

ARGV = sys.argv[sys.argv.index("--") + 1:]

print('Searching .obj\'s from path {0}'.format(ARGV[0]))
if ARGV == None or len(ARGV) == 0:
    raise "No path given\nUsage:\npython meshlab-tinify.py -- /path/to/folder/for/search"

def fix_mtls(path):
    mtls = glob(os.path.dirname(path) + '/**/*.mtl', recursive = True)
    print('Found {0} .mtl\'s, replacing .png with .jpg using sed'.format(len(mtls)))
    for mtl in mtls:
        args = 'sed -i \'s/.png/.jpg/g\' "{0}"'.format(mtl)
        print('Next mtl: {0}'.format(mtl))
        os.system(args)

def fix_pngs(path):
    pngs = glob(os.path.dirname(path) + '/**/*.png', recursive = True)
    print('Found {0} .png\'s, replacing .png with .jpg using imagemagick convert'.format(len(pngs)))
    for png in pngs:
        pngname, pngext = os.path.splitext(png)
        inpng = pngname + pngext
        outjpg = pngname + '.jpg'
        args = 'convert "{0}" -strip -quality 50 "{1}"'.format(inpng, outjpg)
        print('Next png: {0}'.format(png))
        os.system(args)

def reduce_model(path):
    #flags = 'vc vf vq vn vt fc ff fq fn wc wn wt'
    flags = 'vc'
    sizes = {
        '500k': './vert_reduce_to_500k.mlx',
        '1000k': './vert_reduce_to_1000k.mlx',
        '1500k': './vert_reduce_to_1500k.mlx',
    }
    normalize_script = './normalize.mlx'
    infile, inext = os.path.splitext(path)
    processed = []
    for size, size_script in sizes.items():
        old = infile + inext
        new = infile + '_' + size + '.ply'
        log = infile + '.log'
        args = 'meshlabserver -i "{0}" -o "{1}" -m {2} -s {3} -s "{4}" &>> "{5}"'.format(old, new, flags, normalize_script, size_script, log)
        print('Next quality:', new)
        os.system(args)
        processed.append(new)
    return processed

def convert_model_to_babylon(path):
    print('Converting to babylon')
    print('Next:', path)
    infile, inext = os.path.splitext(path)
    babylon = infile + '.babylon'
    log = '/dev/null'
    if os.path.exists(babylon):
        print('.babylon already exists, skipping')
    else:
        print('Blender magic')
        args = 'blender ./blend-convert.blend --background --python ./blender-tinify.py -- "{0}" &>> {1}'.format(path, log)
        os.system(args)


objs = glob(os.path.dirname('{0}/'.format(ARGV[0])) + '/**/*.obj', recursive = True)
objs = [obj for obj in objs if '_small' not in obj and '_medium' not in obj and '_large' not in obj]

print('Found {0} objs'.format(len(objs)))
for i in range(len(objs)):
    obj = objs[i]
    print('######## MODEL {0}/{1} ########'.format(i + 1, len(objs)))
    print('Path:', obj)

    # Check if model has been processed
    current_dir = '{0}'.format(os.path.dirname(obj))
    plys_in_dir = glob('{0}/**/*.ply'.format(current_dir), recursive = True)
    processed = [ply for ply in plys_in_dir if '_small' in ply or '_medium' in ply or '_large' in ply]
    if len(processed) > 0:
        print('Model has been processed. Skipping...')
    else:
        #fix_mtls(obj)
        #fix_pngs(obj)
        processed = reduce_model(obj)

    for new in processed:
        convert_model_to_babylon(new)
