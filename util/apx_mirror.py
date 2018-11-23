#!/usr/bin/env python3
import apx
import sys
import argparse

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_file',  help='input file (.apx)', default=None, nargs='*')
    arg_parser.add_argument('-o', dest='output_file', help='Output file name (default is to overwrite input file)', default=None)
    arg_parser.add_argument('-n', '--name', help='Forces a new name on the mirrored APX node', default=None)
    arg_parser.add_argument('-m', '--normalize', help='Forces APX to be generated in normalized form', action='store_true', default=False)
    arg_parser.add_argument('-p', '--pipe', help='Uses stdin and stdout instead of files', action='store_true', default=False)
    args = arg_parser.parse_args()
    output_file = args.output_file if args.output_file is not None else args.input_file[0]
    
    if args.pipe:
        node = apx.Parser().load(sys.stdin)
    else:
        node = apx.Parser().parse(args.input_file[0])
    node=node.mirror()
    port = None
    if len(node.providePorts) > 0:
       port = node.providePorts
    if args.name is not None:
        node.name = str(args.name)
    if args.pipe:
        print(node.dumps(normalized=args.normalize))
    else:
        node.save_apx(output_file = output_file, normalized=args.normalize)