#!/usr/bin/env python3
import apx
import argparse

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_files',  nargs='+', help='List of APX files')
    arg_parser.add_argument('-n', '--name', help='Name of the new APX node', required=True)
    arg_parser.add_argument('--sort', help='Name of the new APX node', action='store_true', default=False)
    arg_parser.add_argument('--normalize', help='Forces APX to be generated in normalized form', action='store_true', default=False)

    args = arg_parser.parse_args()

    node_list =[]
    parser = apx.Parser()
    for file in args.input_files:
        node_list.append(parser.parse(file))
    if len(node_list) > 0:
        apx_node = apx.Node(args.name)
        for other_node in node_list:
            apx_node.extend(other_node)
    apx_node.finalize(sort=args.sort)
    apx_node.save_apx(normalized=args.normalize)