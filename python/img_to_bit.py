import cv2 as cv
import numpy as np
import getopt, sys
from PIL import Image
import os

'''
This program takes a series of Black and White images
and converts them into strings of bits representing white and black.
'''

# stores the black/white data as a string of 1 and 0
# Each frame is 32x32 pixels
# each line of text will contain 32 characters
# 32 rows will represent one frame

class Error(Exception):
    pass
class NoOutputFile(Error):
    pass
class NoInputFile(Error):
    pass

if __name__ == '__main__':
    # First argument is the path to the python file
    # Others are user inputs
    path = sys.argv[0]
    arguments = sys.argv[1:]
    # print(sys.argv)

    # Options
    options = 'hi:o:'

    # long options
    long_options = ['help', 'input', 'output']

    try:
        # Parse arguments
        arguments, values = getopt.getopt(arguments, options, long_options)
        
        if '-i' not in sys.argv and '-input' not in sys.argv:
            raise NoInputFile
        if '-o' not in sys.argv and '-output' not in sys.argv:
            raise NoInputFile

        # check each argument
        for current_arg, arg_val in arguments:
            if current_arg in ('-h', '--help'):
                print('Displaying Help')

            elif current_arg in ('-i', '--input'):
                print('Input File:', arg_val)
                indir_path = arg_val

            elif current_arg in ('-o', '--output'):
                print('output file:', arg_val)
                outfile_path = arg_val

    except getopt.error as err:
        # error with args
        print(str(err))
    
    except NoOutputFile:
        print('No output file was specified')
        exit()
    except NoInputFile:
        print('No input directory was specified')
        exit()



    # Main Function
    
    # open output file to write to
    with open(outfile_path, 'w') as outfile:

        # open each image in the dir
        for file in sorted(os.listdir(indir_path)):
            img_path = os.path.join(indir_path, file)
            if not os.path.isfile(img_path):
                continue
            print(img_path)
            
            bitstring = ''

            # get image size
            with Image.open(img_path) as img:
                img_width, img_height = img.size
            
                # for each row of pixels
                for h in range(img_height):
                    

                    # for each pixel in the row
                    for w in range(img_width):
                        pixel_value = img.getpixel((w, h))
                        '''
                        if pixel_value == (0, 0, 0):
                            pixel_bit = 0
                        elif pixel_value == (255, 255, 255):
                            pixel_bit = 1
                        else:
                            pixel_bit = 2
                        '''
                        bitstring += str(pixel_value // 255)
                    
                    bitstring += '\n'
                # bitstring += '\n'

            
            outfile.writelines(bitstring)


