#!/usr/bin/python

import os
import argparse
import logging


# Global logger
logger = logging.getLogger("md2rm")


def convert_sharpsign(line):
    # Count the num of hashtag
    count = 0
    for char in line:
        if char is not '#':
            break
        count += 1
     
    # We only cares h1 ~ h6 for the heading
    if count is 0:
        return line
    elif count > 6:
        return line
     
    line = 'h' + str(count) + '. ' + line[count:]
    logger.info("line with heading-switched is " + line)
        
    return line
# end convert_sharpsign

def convert_asterisk(line):
    if '*' in line:
        index = line.find('*')
        logger.info("found the asterisk at : " + str(index))
        if line[index+1] is not ' ': # in this case, it's for emphasis
            return line
        
    # Fill the previous blanks with asterisk: One asterisk for two blanks
    line = '*' * (index/2) + line[index:]
    return line
# end convert_asterisk 

def interpret_line(line):
    # Handle Heading in Markdown (2 ways: h#, ===== or ----- )
    # Check 'sharpsign(#)' symbol
    if line[0] is '#':
        line = convert_sharpsign(line)

    # Check heading-indicating line
    # TODO: Impl heading-indicating line check

    # Handle 'Asterisk(*)' symbol
    # TODO: Impl conversion of asteroid 
    if line[0] is '#' or line[0] is ' ':
        line = convert_asterisk(line)
        
    return line
# end interpret_line 


def convert_markdown(inputFile, outname=None):
    # Check input file validity
    if not os.path.isfile(inputFile):
        logger.error("Input file is not valid.")
        exit()

    if outname is None:
        logger.info("Outputfile name is not set.")
        # set output name with inputfile name, 
        # which is replaced with rm(redmine) extesion.
        _output, ext = os.path.splitext(inputFile)
        logger.info("file : " + _output + " and, extension: " + ext)
        _output = _output + ".rm"
    else:
        _output = outputname

    _input = inputFile
    # Logging output filename
    logger.info("Input filename is : " + _input)
    logger.info("Output filename is : " + _output)


    # Open the file for input and output
    f_in = open(_input, "r")
    f_out = open(_output, "w")

    while True:
        # Read the lines one by one
        # TODO: need to check the blank empty line
        line = f_in.readline()

        # If it reaches the end of file, escape
        if not line: 
            break
        line = interpret_line(line)

        f_out.write(line)
       
    # Close the open files
    f_in.close()
    f_out.close()

    return
# end convert_markdown 


# ================================ MAIN FUNC ================================ 
if __name__ == '__main__':
    # Arugment parsing
    parser = argparse.ArgumentParser()

    parser.add_argument("--filename", required=True, help="Input filename.")
    parser.add_argument("--outname", required=False, help="Output filename.")

    args = parser.parse_args()


    # Set logging
    logger.setLevel(logging.FATAL)

    # Logging handler
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    # Logging formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')
    
    logger.info("Program start")
    convert_markdown(args.filename, args.outname)


