#!/usr/bin/env python3
import sys
import apx
import argparse

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_file',  nargs='*', help='Path to input file (.apx)')
    arg_parser.add_argument('-o', dest='output_file', help='Output file name (default is to overwrite input file)', default=None)
    arg_parser.add_argument('-p', '--pipe', help='Uses stdin and stdout instead of files', action='store_true', default=False)
    args = arg_parser.parse_args()
    if len(args.input_file) == 0 and not args.pipe:
        arg_parser.print_help()
        sys.exit(1)

    output_file = args.output_file if args.output_file is not None else args.input_file[0]
    
    if args.pipe:
        node = apx.Parser().load(sys.stdin)
        print(node.dumps(normalized=False))
    else:
        node = apx.Parser().parse(args.input_file[0])
        node.save_apx(output_file = output_file, normalized=False)