#!/bin/python3

import re
import sys

PROG_NAME = 'offset_tmp_subs'


def print_usage():
    print(f'usage: {PROG_NAME} OFFSET SUBTITLE_FILE OUTPUT_FILE')
    print('Delay subtitles in MTP format by OFFSET number of seconds.')


def main(prog_name, *args):
    if len(sys.argv) != 3:
        arg_count = len(args)
        print(
            f'{PROG_NAME}: Wrong number of arguments.',
            'Required 3, but found {arg_count}'
        )
        print_usage()
        exit(1)
    offset = int(args[0])
    subtitle_fname = args[1]
    output_fname = args[2]
    with open(subtitle_fname) as subtitle_file:
        subtitle_file_lines = list(subtitle_file)


if __name__ == '__main__':
    main(sys.argv)
