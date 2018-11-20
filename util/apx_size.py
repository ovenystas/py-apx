#!/usr/bin/env python3

import apx
import sys, os

if __name__ == "__main__":
    with open(sys.argv[1]) as fp:
        node = apx.Parser().load(fp)
        inDataSize = sum([port.dsg.packLen() for port in node.requirePorts])
        outDataSize = sum([port.dsg.packLen() for port in node.providePorts])        
        print("in:\t{:d}\tout:\t{:d}".format(inDataSize, outDataSize))