"""
input files look like configuration files
[*.py]
indent_style = space
indent_size = 4

[*.js]
indent_style = space
indent_size = 2

$python ini2csv.py .editorconfig ini2csv.csv
csv file looks like this:
*.py,indent_style,space
*.py,indent_size,4
*.js,indent_style,space
*.js,indent_size,2

with --collapsed argument, csv file looks like this
header,indent_style,indent_size
*.py,space,4
*.js,space,2
"""

import csv
from configparser import ConfigParser
from argparse import ArgumentParser, FileType
from functools import partial


parser = ArgumentParser(description="convert ini to csv.", epilog='By Shuchen Wu')
parser.add_argument('input_file', type=FileType('r'))
parser.add_argument('output_file', type=partial(open, mode='w', newline=''))
parser.add_argument('--collapsed', action='store_true', help="collapse the rows to one row per section")
# args = parser.parse_args(['.editorconfig', 'ini2csv.csv', '--collapsed'])
args = parser.parse_args()
config = ConfigParser()
config.read_file(args.input_file)

if args.collapsed:
    headers = ('header',) + tuple((config.options(config.sections()[0])))

    rows = (
        {'header': name, **section}
        for name, section in config.items()
        if section
    )

    csv_writer = csv.DictWriter(args.output_file, fieldnames=headers)
    csv_writer.writeheader()
    csv_writer.writerows(rows)
else:
    csv_writer = csv.writer(args.output_file)
    csv_writer.writerows(
        [name, key, value]
        for name, section in config.items()
        for key, value in section.items()
    )
