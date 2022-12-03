#!/bin/python3

import re
import sys

PROG_NAME = 'offset_tmp_subs'
SUBTITLE_LINE_PATTERN = re.compile(r'(\d+:\d\d:\d\d)([:=])(.*)')
TIMESTAMP_PATTERN = re.compile(r'(\d+):(\d\d):(\d\d)')
OFFSET_TIME_PATTERNS = {
        'ONLY SECONDS': re.compile(r'[-+]?\d+'),
        'WITH MINUTES': re.compile(r'([-+])?(\d\d):(\d\d)'),
        'WITH HOURS': re.compile(r'([-+])?(\d+):(\d\d):(\d\d)')
}


def print_usage():
    print(f'usage: {PROG_NAME} OFFSET SUBTITLE_FILE OUTPUT_FILE')
    print('Delay or hasten subtitles in MTP format by OFFSET number of seconds.')
    print('OFFSET can be a signed number of seconds or a time string similar')
    print('to: -01:30, +02:00, or 01:23:45.')


def main(prog_name, *args):
    if len(args) != 3:
        print(
            f'{PROG_NAME}: Wrong number of arguments.',
            f'Required 3, but found {len(args)}'
        )
        print_usage()
        exit(1)
    offset_string = args[0]
    subtitle_fname = args[1]
    output_fname = args[2]
    offset = total_seconds(offset_string)
    with open(subtitle_fname) as subtitle_file:
        subtitle_file_lines = list(subtitle_file)
    with open(output_fname, 'x') as output_file:
        for line in offset_subtitles(subtitle_file_lines, offset):
            print(line, file=output_file)


"""Convert a timestamp string with hours, minutes, and seconds to a total
number of seconds:

    >>> timestamp_to_seconds('02:10:39')
    7839

You can omit hours and seconds:

    >>> timestamp_to_seconds('01:10')
    70
    >>> timestamp_to_seconds('120')
    120
"""

def total_seconds(offset_string):
    """Convert a timestamp string with hours, minutes, and seconds to a total
    number of seconds:

        >>> total_seconds('02:10:39')
        7839

    You can omit hours and seconds:

        >>> total_seconds('01:10')
        70
        >>> total_seconds('120')
        120

    Argument may be signed:

        >>> total_seconds('-01:02:03')
        -3723
        >>> total_seconds('+03:55')
        235
    """
    if match := OFFSET_TIME_PATTERNS['ONLY SECONDS'].fullmatch(offset_string):
        return int(offset_string)
    elif match := OFFSET_TIME_PATTERNS['WITH MINUTES'].fullmatch(offset_string):
        sign = -1 if match.groups()[0] == '-' else 1
        minutes = int(match.groups()[1])
        seconds = int(match.groups()[2])
        return (minutes * 60 + seconds) * sign
    elif match := OFFSET_TIME_PATTERNS['WITH HOURS'].fullmatch(offset_string):
        sign = -1 if match.groups()[0] == '-' else 1
        hours = int(match.groups()[1])
        minutes = int(match.groups()[2])
        seconds = int(match.groups()[3])
        return (hours * 3600 + minutes * 60 + seconds) * sign
    else:
        raise ValueError(f'bad time offset string {offset_string!r}')


def offset_subtitles(lines, seconds):
    """Delay/hasten timestamps of lines in format of TMPlayer subtitle file.

        >>> subs = [
        ...     "00:26:18:I'm a liar, a hypocrite.",
        ...     "00:26:21:I'm afraid of everything|I don't ever tell the truth.",
        ...     "00:26:25:I don't have the courage.",
        ...     "00:26:29:When I see a woman, I blush and look away.",
        ...     "00:26:32:I want her, but I don't take her... for God.",
        ... ]
        >>> for line in offset_subtitles(subs, 5):
        ...     print(line)
        ... 
        00:26:23:I'm a liar, a hypocrite.
        00:26:26:I'm afraid of everything|I don't ever tell the truth.
        00:26:30:I don't have the courage.
        00:26:34:When I see a woman, I blush and look away.
        00:26:37:I want her, but I don't take her... for God.
        >>> 

    If senconds argument is negative, subtitles that would have to appear
    before 00:00:00 moment, will be excluded from the result:

        >>> subs = [
        ...     '00:00:10=Translation & sync by luciferdisciple',
        ...     '00:00:30=Long, long time ago|in a land far, far away...'
        ... ]
        >>> for line in offset_subtitles(subs, -20):
        ...     print(line)
        ... 
        00:00:10=Long, long time ago|in a land far, far away...
        >>> 
    """
    for line in lines:
        fixed_line = offset_line(line, seconds)
        if fixed_line.startswith('-'):
            continue
        yield fixed_line


def offset_line(line, seconds):
    """Offset timestamp of a single line.

        >>> offset_line('00:00:50:This is the Earth|at a time when', -15)
        '00:00:35:This is the Earth|at a time when'
        >>> offset_line(
        ...     "00:26:29=I want her, but I don't take her... for God.",
        ...     555)
        "00:35:44=I want her, but I don't take her... for God."
    """
    timestamp, separator, content = SUBTITLE_LINE_PATTERN.match(line).groups()
    fixed_timestamp = offset_timestamp(timestamp, seconds)
    return f'{fixed_timestamp}{separator}{content}'


def offset_timestamp(timestamp, seconds):
    """
        >>> offset_timestamp('00:30:00', -11)
        '00:29:49'
        >>> hours, minutes, seconds = 2, 7, 45
        >>> total_seconds = (hours * 60 * 60) + (minutes * 60) + seconds
        >>> offset_timestamp('1:55:30', total_seconds)
        '04:03:15'
    """
    match = TIMESTAMP_PATTERN.match(timestamp)
    init_hour, init_min, init_sec = match.groups()
    init_hour = int(init_hour)
    init_min = int(init_min)
    init_sec = int(init_sec)
    total_seconds = init_hour * 60 * 60 + init_min * 60 + init_sec
    total_seconds += seconds
    second = total_seconds % 60
    total_minutes = total_seconds // 60
    minute = total_minutes % 60
    hour = total_minutes // 60
    return f'{hour:02d}:{minute:02d}:{second:02d}'


if __name__ == '__main__':
    main(*sys.argv)
