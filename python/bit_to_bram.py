import os, getopt, sys

'''
This program takes file containing the bits representing the
black and white image(s) and turns it into a verilog module.
Format based of https://embeddedthoughts.com/2016/07/30/storing-image-data-in-block-ram-on-a-xilinx-fpga/.

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
                infile_path = arg_val

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
        print('No input file was specified')
        exit()



    # Main Function

    address_bits = 16
    data_bits = 32
    frame_limit = 18
    
    # open output file to write to
    with open(outfile_path, 'w') as outfile:

        # write the beginning part of the module
        intro = ['module bad_apple_rom(\n',
                 '\tinput clk,\n',
                 f'\tinput [{address_bits-1}:0] address,\n',
                 f'\toutput reg [{data_bits-1}:0] data\n',
                 '\t);\n',
                 '\n',
                 '\t(* rom_style = \"block\" *)\n',
                 '\n',
                 '\t// signal declaration\n'
                 f'\treg [{address_bits-1}:0] address_reg;\n',
                 '\n',
                 '\talways @(posedge clk)\n',
                 '\t\tbegin\n',
                 '\t\taddress_reg <= address;\n',
                 '\t\tend\n',
                 '\n',
                 '\talways @*\n',
                 '\tcase(address)\n']
        outfile.writelines(intro)


        # write the main data (this part will be very long)
        with open(infile_path) as infile:

                current_address = 0

                # loop over every line
                for line in infile:
                    i = 0
                    if i == frame_limit * 8:
                        break
                    outfile.write('\t\t')

                    # write the current address in binary
                    outfile.write(f'{address_bits}\'d{current_address:05}: data = ')
                    # write the data associated with that address
                    outfile.write(f'{data_bits}\'b{str.strip(line)};\n')

                    current_address += 1

                    i += 1

        
        # write the rest of the module
        outfile.write(f'\t\tdefault: data = {data_bits}\'b{data_bits * str(0)};\n')
        outfile.write('\tendcase\nendmodule\n')
