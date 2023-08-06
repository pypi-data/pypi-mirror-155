#!/usr/bin/env python
"""
Utility to redact sensitive data
"""

import argparse

from gtredactkit.redact import Redactor
from gtredactkit.unredact import Unredactor
import os
import glob
import sys

# Creating instances of redact and unredact classes
redact_obj = Redactor()
unredact_obj = Unredactor()


banner = r"""

  ________ __    __________           .___              __     ____  __.__  __   
 /  _____//  |_  \______   \ ____   __| _/____    _____/  |_  |    |/ _|__|/  |_ 
/   \  __\   __\  |       _// __ \ / __ |\__  \ _/ ___\   __\ |      < |  \   __\
\    \_\  \  |    |    |   \  ___// /_/ | / __ \\  \___|  |   |    |  \|  ||  |  
 \______  /__|    |____|_  /\___  >____ |(____  /\___  >__|   |____|__ \__||__|  
        \/               \/     \/     \/     \/     \/               \/                                                                                   
                    +-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+
                    |P|o|w|e|r|e|d| |b|y| |B|r|o|o|t|w|a|r|e|
                    +-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+
            
    https://github.com/brootware
    https://brootware.github.io                                                                             
    """

help_menu = """
    GtRedactKit - Redact and Un-redact any sensitive data from your text files!
    Example usage:\n
        redactor 'This is my ip: 127.0.0.1. My email is brute@gmail.com'\n
        redactor --file [file/filestoredact]\n
        redactor --file redacted_file --unredact .hashshadow.json\n
        redactor --file file --customfile custom.json\n
    """


def arg_helper() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Supply a sentence or paragraph to redact sensitive data from it. Or read in a file or set of files with -f to redact",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "text",
        type=str,
        help="""Redact sensitive data of a sentence from command prompt.""",
        nargs="*"
    )
    if len(sys.argv) == 1:
        print(help_menu)
        parser.print_help(sys.stderr)
        sys.exit(1)
    parser.add_argument(
        "-f",
        "--file",
        nargs="+",
        help="""Path of a file or a directory of files."""
    )
    parser.add_argument(
        "-u",
        "--unredact",
        help="""
                Option to unredact masked data.
                Usage: redactor -f [redacted_file] -u [.hashshadow.json]
                """
    )
    parser.add_argument(
        "-d",
        "--dirout",
        help="""
                Output directory of the file.
                Usage: redactor -f [file/filestoredact] -d [redacted_dir]
                """
    )
    parser.add_argument(
        "-c",
        "--customfile",
        help="""
                User defined custom regex pattern for redaction.
                Usage: redactor -f [file/filestoredact] -c [customfile.json]
                """
    )
    parser.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        default=True,
        help='Search through subfolders'
    )
    parser.add_argument(
        '-e',
        '--extension',
        default='',
        help='File extension to filter by.'
    )
    args = parser.parse_args()

    return args


def execute_file_arg() -> None:
    args = arg_helper()
    full_paths = [os.path.join(os.getcwd(), path) for path in args.file]
    files = set()

    for path in full_paths:
        if os.path.isfile(path):
            file_name, file_ext = os.path.splitext(path)
            if args.extension in ('', file_ext):
                files.add(path)
        elif args.recursive:
            full_paths += glob.glob(path + '/*')

    for file in files:
        if args.customfile and args.dirout:
            redact_obj.process_custom_file(file, args.customfile, args.dirout)
            redact_obj.process_report(file)
        elif args.customfile:
            redact_obj.process_custom_file(file, args.customfile)
            redact_obj.process_report(file)
        elif args.dirout:
            redact_obj.process_core_file(file, args.dirout)
            redact_obj.process_report(file, args.dirout)
        elif args.unredact:
            unredact_obj.unredact(file, args.unredact)
        else:
            redact_obj.process_core_file(file)
            redact_obj.process_report(file)


def main():
    print(banner)

    args = arg_helper()
    if args.file or (args.file and args.dirout):
        execute_file_arg()
    else:
        redact_obj.process_text(args.text)


if __name__ == "__main__":
    main()
