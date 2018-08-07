#!/usr/bin/env python

'''
This is a python script to format a input text from standard input
based on the stars(*) or dots(.) present at the beginning of each line(optional).
Here * will act as index numbering system and . will act as sub section of
each index and +/- signs will be used to represent if it can be expanded further
or not.

Author : mathewjose09@gmail.com
Date : 07-Aug-2018

'''

import re
import sys

# f = open('input.txt', 'r')
# Global variables to be used in the calls across formatting functions
star_pattern = re.compile('\*+')
dot_pattern = re.compile('\.+')
current_main_number = 0
current_sub_numbering = '0'
previous_star_sequence = ""
previous_sub_block = []


def get_index_numbering(current_star_sequence):
    '''
    This function will find out the next sequence numbering in the output text (like 1.1, 3.2.1 etc).
    :param current_star_sequence: current star sequence from beginning of the line.
    :return: next index numbering to be used in the output.
    '''
    global current_main_number
    global previous_star_sequence
    global current_sub_numbering

    # Checking if its a new block like 1,2,3 etc if the line is starting with a single *
    if current_star_sequence == '*':
        current_main_number += 1
        # storing the sub numbering in each block to be easily used later like 1.1,1.2,2.1 etc.
        current_sub_numbering = str(current_main_number)
        previous_star_sequence = current_star_sequence
        return str(current_main_number)
    else:
        prev_star_length = len(previous_star_sequence)
        current_star_length = len(current_star_sequence)

        # Checking if it is extending a existing sub numbering like 2.1 to 2.1.1 or 3.1.1 to 3.1.1.1
        if current_star_length > prev_star_length:
            current_sub_numbering += '.' + '1'
        # starting a new sub sequencing under a main block number .
        # means if the number of stars in current line is less than the previous stars then a new sub sequence is needed
        # ex : if we are in 2.1.1 with (***) and a new line comes with (**) then 2.2 sub sequence need to be started
        else:
            new_sub_num = ".".join(str(current_sub_numbering).split(".")[:current_star_length])
            new_seq = int(str(new_sub_num).split(".")[-1]) + 1
            current_sub_numbering = ".".join(str(new_sub_num).split(".")[:current_star_length - 1]) + '.' + str(new_seq)
        previous_star_sequence = current_star_sequence
        return current_sub_numbering

    return str(current_sub_numbering)


def process_prev_sub_block():
    '''
    This will process the all lines in each of the main index blocks like 1,2,3 etc in one go
    :return: None
    '''
    global previous_sub_block
    dot_length = 0
    if previous_sub_block:
        len_sub_block = len(previous_sub_block)
        for pos, data in enumerate(previous_sub_block):
            data = data.strip("\n")
            is_plus_needed = False

            # if lines starts with '.' then it needs to be checked for formatting with +/- based on the lines following it
            if data.startswith('.'):
                dot_sequence = dot_pattern.match(data)
                dot_length = len(dot_sequence.group())
                sub_dot_sequence = "." * (dot_length + 1)
                data = data.lstrip('.')
                if pos < len_sub_block - 1:
                    # Check the remaining lines in the current block to see if the current line needs a +
                    for remaining_data in previous_sub_block[pos + 1:]:
                        if remaining_data.startswith(sub_dot_sequence):
                            is_plus_needed = True
                            break
                        # Break if you see a remaining line dot sequence ,same as current examining lines dot length.
                        # Since it cant be a + sign for the current examining line .
                        if remaining_data.startswith(dot_sequence.group()):
                            break

                    if is_plus_needed:
                        print(' ' * dot_length + '+' + data)
                    else:
                        print(' ' * dot_length + '-' + data)
                else:
                    print(' ' * dot_length + '-' + data)
            else:
                # for handling if a text spans multiple lines
                print(' ' * (dot_length + 2) + data)
        previous_sub_block = []


# Process the lines from STDIN line by line
for line in sys.stdin:
    line = line.strip('\n')
    if not line.isspace() and line:
        star_sequence = star_pattern.match(line)
        if star_sequence:
            process_prev_sub_block()
            current_star_sequence = star_sequence.group()
            index_numbering = get_index_numbering(current_star_sequence)
            print(index_numbering + line.lstrip('*'))
        else:
            # If it is not a main block ,keep tracking the lines to process together once we reach the next main block.
            previous_sub_block.append(line)

# For processing last block
process_prev_sub_block()
