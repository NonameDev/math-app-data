from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import shutil
import json
import sys
import os

IMGS_ROOT_PATH = './imgs'
DIR_FORMAT = '{0}/{1}'
"""
DPI info is defined here. The key referes to the name and the value refers
to the font size used when generating the image.
NOTE: These might need to be tweaked after further testing
"""
DPI = dict(ldpi=30,
           mdpi=75,
           hdpi=150,
           xhdpi=300)


def main():
    """
    Method called when script is run. Parses the equation
    data and generates images for all the equations
    """
    check_imgs_dir()
    with open('data/equation_data.json') as eqn_data_file:
        eqn_data = json.load(eqn_data_file)
        eqns = eqn_data['equations']
        tmp_dir = tempfile.mkdtemp()
        for size_name in DPI:
            gprint('Generating {0} images'.format(size_name))
            for eqn in eqns:
                tex = eqn['tex']
                out_name = '{0}.png'.format(eqn['image_key'])
                generate_image(out_name, tex, tmp_dir, size_name)
                gprint('\tGenerated img {0}'.format(out_name))
        shutil.rmtree(tmp_dir)


def gprint(s):
    """
    Allows the script to print directly to the terminal while script is being
    executed through Gradle by flushing stdout as mentioned in the following
    StackOverflow answer
    http://stackoverflow.com/a/28194508/2392229

    @type  s: string
    @param s: string that will be printed
    """
    print(s)
    sys.stdout.flush()


def check_imgs_dir():
    """
    Checks if the imgs directory (and all its subdirectories) exists and if it
    doesnt, it creates it
    """
    check_dir(IMGS_ROOT_PATH)
    for size_name in DPI:
        path = DIR_FORMAT.format(IMGS_ROOT_PATH, size_name)
        check_dir(path)


def check_dir(path):
    """
    Checks if the directory at the given path exists. If it doesnt, the
    directory is created

    @type  path: string
    @param path: sting containing the path to the directory being checked
    """
    if not os.path.exists(path):
        os.mkdir(path)


def generate_image(out_name, tex, tmp_dir, size_name):
    """
    Generates an image with the give filename(out_name) for the
    given tex string

    @type  out_name: string
    @param out_name: string containing the filename of the
                     resulting image
    @type  tex: string
    @param tex: string containing the tex used to generate the
                image
    @type  tmp_dir: string
    @param tmp_dir: string containing path to the temporary
                    directory used to save the raw image
                    from matplotlib
    @type  size_name: string
    @param size_name: string containing the name of the size of the image
    """
    tmp_filename = '{0}/{1}'.format(tmp_dir, 'tmp.png')
    plt.text(0,
             0,
             r"$%s$" % tex,
             fontsize=DPI[size_name])
    plt.axis('off')
    plt.savefig(filename=tmp_filename,
                transparent=True,
                dpi=100,
                bbox_inches='tight',
                pad_inches=0)
    trim_img(out_name, tmp_filename, size_name)
    plt.clf()


def trim_img(out_name, filename, size_name):
    """
    Crops the whitespace in the temporary image generated

    @type  out_name: string
    @param out_name: string containing the filename of the
                     resulting image
    @type  filename: string
    @param filename: filename of the temporary image
    @type  size_name: string
    @param size_name: string containing the name of the size of the image
    """
    out_dir = DIR_FORMAT.format(IMGS_ROOT_PATH, size_name)
    full_out_name = DIR_FORMAT.format(out_dir, out_name)
    im = Image.open(filename)
    pix = np.asarray(im)

    pix = pix[:, :, 0:3]
    idx = np.where(pix-255)[0:2]
    box_min = list(map(min, idx))[::-1]
    box_max = list(map(max, idx))[::-1]
    box = box_min + box_max

    region = im.crop(box)
    region.save(full_out_name, 'PNG')

if __name__ == '__main__':
    main()
