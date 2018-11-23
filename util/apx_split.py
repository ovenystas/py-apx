#!/usr/bin/env python3
import os, sys
import apx
import argparse

def parse_lines_in_file(path):
    """
    Parses text file path line by line and returns a list of names found in it.
    The special character '#' can be used as a comment character and allows users to write line comments.
    Comments does not affect what this function returns.
    """
    signals = []
    with open(path) as fp:
        for line in fp:
            # removes all text comments starting with # character
            parts = line.partition('#')
            line = parts[0]

            # removes starting and ending whitespace
            line = line.strip()
            if len(line) > 0:
                signals.append(line)
    return signals

def create_apx_node_from_file_name(file_name, default_name):
    if file_name is None:
        node_name = default_name
    else:
        node_name = os.path.basename(file_name)
        if '.apx' in node_name:
            node_name = os.path.splitext(node_name)[0]
    return apx.Node(node_name)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_file', help='The APX file to split (.apx)')
    arg_parser.add_argument('port_names', nargs='*', help="Port names to be included in head")
    arg_parser.add_argument('--head', help='APX File to write head result (.apx)', default=None)
    arg_parser.add_argument('--tail', help='APX file to write tail result (.apx)', default=None)
    arg_parser.add_argument('--head_name', help='Force new name of head APX node', default='Head')
    arg_parser.add_argument('--tail_name', help='Force new name of head APX node', default='Tail')
    arg_parser.add_argument('--file', help='Read port names from file instead', default=None)
    arg_parser.add_argument('--sort', help='Name of the new APX node', action='store_true', default=False)
    arg_parser.add_argument('--mirror', help='Forces output of head and tail to be mirrored', action='store_true', default=False)


    args = arg_parser.parse_args()
    if args.file is None and len(args.port_names)==0:
        arg_parser.print_help()
        sys.exit(1)

    head_node = create_apx_node_from_file_name(args.head, args.head_name)
    if args.tail is not None:
        tail_node = create_apx_node_from_file_name(args.tail, args.tail_name)
    else:
        tail_node = None
    source_node = apx.Parser().parse(args.input_file)

    if args.file is not None:
        port_names = parse_lines_in_file(args.file)
    else:
        port_names = args.port_names

    processed = set()
    for name in port_names:
        source_port = source_node.find(name)
        if (source_port is not None) and (source_port.name not in processed):
            processed.add(source_port.name)
            head_node.add_port_from_node(source_node, source_port)

    if args.mirror:
        head_node=head_node.mirror()
    head_node.finalize(args.sort)
    if args.head is not None:
        head_node.save_apx(output_file=args.head, normalized=True)
    else:
        print(head_node.dumps(normalized=True))

    if tail_node is not None:
        if args.mirror:
            tail_node=tail_node.mirror()
        head_node.finalize(args.sort)
        for source_port in source_node.providePorts+source_node.requirePorts:
            if source_port.name not in processed:
                tail_node.add_port_from_node(source_node, source_port)
        tail_node.save_apx(output_file=args.tail, normalized=True)



