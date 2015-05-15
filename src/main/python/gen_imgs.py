from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import shutil
import json
import os


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
        for eqn in eqns:
            tex = eqn['tex']
            out_name = '{0}.png'.format(eqn['image_key'])
            generate_image(out_name, tex, tmp_dir)
            print('Generated img {0}'.format(out_name))
        shutil.rmtree(tmp_dir)


def check_imgs_dir():
    """
    Checks if the imgs directory exists and if it
    doesnt, it creates it
    """
    if not os.path.exists('./imgs'):
        os.mkdir('./imgs')


def generate_image(out_name, tex, tmp_dir):
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
    """
    tmp_filename = '{0}/{1}'.format(tmp_dir, 'tmp.png')
    plt.text(0,
             0,
             r"$%s$" % tex,
             fontsize=300)
    plt.axis('off')
    plt.savefig(filename=tmp_filename,
                transparent=True,
                dpi=100,
                bbox_inches='tight',
                pad_inches=0)
    trim_img(out_name, tmp_filename)
    plt.clf()


def trim_img(out_name, filename):
    """
    Crops the whitespace in the temporary image generated

    @type  out_name: string
    @param out_name: string containing the filename of the
                     resulting image
    @type  filename: string
    @param filename: filename of the temporary image
    """
    dir_out_name = 'imgs/{0}'.format(out_name)
    im = Image.open(filename)
    pix = np.asarray(im)

    pix = pix[:, :, 0:3]
    idx = np.where(pix-255)[0:2]
    box_min = list(map(min, idx))[::-1]
    box_max = list(map(max, idx))[::-1]
    box = box_min + box_max

    region = im.crop(box)
    region.save(dir_out_name, 'PNG')

if __name__ == '__main__':
    main()
