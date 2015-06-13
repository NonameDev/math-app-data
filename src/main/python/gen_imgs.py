from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import threading
import tempfile
import shutil
import json
import sys
import os

GENERATED_IMAGE_FORMAT = '[thread:{0} | dpi:{1}] Generated img {2}'
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
        workers = []
        for size_name in DPI:
            worker = ImageGenerator(eqns, size_name)
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
        verify_output(eqns)


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


def verify_output(eqns):
    """
    Verifies that the output of the script is correct

    @type  eqns: list
    @param eqns: Equations exracted from the equation data file
    """
    for size_name in DPI:
        path = DIR_FORMAT.format(IMGS_ROOT_PATH, size_name)
        if not verify_dpi_dir(path, eqns):
            raise Exception('Failed validity test!!!!')


def verify_dpi_dir(path, eqns):
    """
    Verifies that the given dpi directory contains all the expected images

    @type  path: string
    @param path: path to the dpi directory
    @type  eqns: list
    @param eqns: Equations exracted from the equation data file
    """
    for eqn in eqns:
        image_name = '{0}.png'.format(eqn['image_key'])
        image_path = DIR_FORMAT.format(path, image_name)
        if not os.path.isfile(image_path):
            return False
    return True


class ImageGenerator(threading.Thread):
    """
    Class in charge of generating the images for a DPI level
    """

    def __init__(self, eqns, size_name):
        """
        Constructor. Sets the given parameters to instance variables and
        creates a new matplotlib figure for the given DPI level

        @type  eqns: list
        @param eqns: Equations exracted from the equation data file
        @type  size_name: string
        @param eqns: Name of the DPI level whose images are being generated
        """
        super(ImageGenerator, self).__init__()
        self._eqns = eqns
        self._size_name = size_name
        self._fig = plt.figure()

    def run(self):
        """
        Iterated through the equations and generates an image for each one
        """
        tmp_dir = tempfile.mkdtemp()
        for eqn in self._eqns:
            tex = eqn['tex']
            out_name = '{0}.png'.format(eqn['image_key'])
            self.generate_image(out_name, tex, tmp_dir, self._size_name)
            self.print_generated_image(out_name)
        plt.close(self._fig)
        shutil.rmtree(tmp_dir)

    def print_generated_image(self, out_name):
        """
        Prints to the terminal to show that the image with the given name has
        been generated

        @type  out_name: string
        @param out_name: Name of the image generated
        """
        gprint(GENERATED_IMAGE_FORMAT.format(threading.current_thread().ident,
                                             self._size_name,
                                             out_name))

    def generate_image(self, out_name, tex, tmp_dir, size_name):
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
        fig_index = abs(hash(tmp_filename)) % 100
        self._fig = plt.figure(fig_index)
        self._fig.text(0,
                       0,
                       r"$%s$" % tex,
                       fontsize=DPI[size_name])
        self._fig.savefig(filename=tmp_filename,
                          transparent=True,
                          dpi=100,
                          bbox_inches='tight',
                          pad_inches=0)
        self.trim_img(out_name, tmp_filename, self._size_name)
        plt.close(self._fig)

    def trim_img(self, out_name, filename, size_name):
        """
        Crops the transparent whitespace in the temporary image generated and
        saves it in the given path

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
        img = Image.open(filename)
        img_array = np.asarray(img)
        # isolate alpha bytes in the image array
        img_array_alpha = img_array[:, :, -1:]
        # find all non-transparent points in the image
        non_transparent_points = np.where(img_array_alpha != 0)[0:2]
        min_crop = list(map(min, non_transparent_points))[::-1]
        max_crop = list(map(max, non_transparent_points))[::-1]
        crop = min_crop + max_crop
        cropped_image = img.crop(crop)
        cropped_image.save(full_out_name, 'PNG')

if __name__ == '__main__':
    main()
