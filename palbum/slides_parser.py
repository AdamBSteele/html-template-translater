import sys
import argparse
import shutil
import os
from bs4 import BeautifulSoup
from folder_structure import folder_structure
from index import index
from slides_maker import slides_image_urls
import re
import threading


class image_to_html:

    '''
    This is the main method where the execution
    starts.
    '''

    def __init__(self, dir, selection):
        self.images = []
        self.threads = []
        self.slides_path = ""
        self.c_dir = ""
        self.dir = dir
        self.selection = selection
        self.working_directory = os.getcwd()
        os.chdir(os.path.abspath(dir))
        self.album_name = (os.path.abspath(dir)).split(os.sep)[-1]
        self.album_path = ""

    def append_images(self):
        '''
        This method appends all the images to a list which
        will be used through out the class.
        '''
        for file in os.listdir(self.dir):
            if file.endswith(".jpg"):
                self.images.append(file)

    def images_to_html_threads(self):
        for imageIndex, image in enumerate(self.images):
            '''The below file open operation takes place every time
            when the for loop iterates (I know doing this operation
            every time in a for loop is bad). I tried it by declaring
            it as global varibale. But the problem with global variable
            is -- BeautifulSoup is maintaining its state even though the
            global data is passed several times.

            Briefly, the result which comes in the first loop is repeating
            again and again through out the loop.

            For this reason, we have put up the open operation in the for
            loop itself'''
            htt_file = open(os.path.join(self.c_dir, "slide.htt"), 'r')
            soup = BeautifulSoup(htt_file)
            im = ""
            if imageIndex > 0 and imageIndex < (len(self.images) - 1):
                previousimage = self.images[imageIndex - 1]
                im = self.images[imageIndex]
                nextimage = self.images[imageIndex + 1]
            elif imageIndex > 0 and imageIndex == (len(self.images) - 1):
                previousimage = self.images[imageIndex - 1]
                im = self.images[imageIndex]
                nextimage = ""
            elif imageIndex > 0 and imageIndex > (len(self.images) - 1):
                break
            else:
                previousimage = ""
                im = self.images[imageIndex]
                nextimage = self.images[imageIndex + 1]
            new_thread = slides_image_urls(
                soup, previousimage, im, nextimage,
                self.album_name, self.slides_path)
            new_thread.start()
            self.threads.append(new_thread)
            htt_file.close()
        htt_file1 = open(os.path.join(self.c_dir, "index.htt"), 'r')
        sp = BeautifulSoup(htt_file1)
        index_create = index(sp, self.album_path, self.images, self.album_name)
        index_create.index_parser()
        htt_file1.close()
        for t in self.threads:
            t.join()

    def image_retrieve(self):
        '''
        This method helps in cresting the output folder
        structure of our album. It also helps in retrieving all
        the images from the folder path which we have given
        as an argument. After creating the whole folder structure,
        the code helps in copying the whole images and the required
        files of the template to the output folder.
        '''

        fs = folder_structure(self.dir, self.working_directory, self.selection)
        self.slides_path, self.album_path = fs.create_folder_structure()
        self.append_images()
        p_dir = os.path.abspath(
            os.path.join(self.working_directory, os.pardir))
        self.c_dir = os.path.join(p_dir, "Minimal")
        self.images_to_html_threads()

        fs = folder_structure(self.dir, self.working_directory, self.selection)
        self.slides_path, self.album_path = fs.create_folder_structure()
        self.append_images()
        p_dir = os.path.abspath(os.path.join(
            self.working_directory, os.pardir))
        self.c_dir = os.path.join(p_dir, "Minimal")
        self.images_to_html_threads()


if __name__ == "__main__":
    '''
    The main method where the execution starts and goes to
    the next level. In this, argparser has been implemented
    as you have to give the directory path of the images with
    a -d option.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Creates html pages " +
                        "for the images in the given argument(directory)",
                        type=str, nargs='+')
    args = parser.parse_args()
    if args.directory is not None:
        if os.path.isdir(args.directory[0]) and args.directory[1] is not None:
            i_to_h = image_to_html(args.directory[0], args.directory[1])
            i_to_h.image_retrieve()
        else:
            print(
                "You haven't entered any valid directory" +
                "path (or) you haven't given the second " +
                "argument (light or dark)")
            sys.exit()
