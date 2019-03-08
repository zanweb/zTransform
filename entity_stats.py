#!/usr/bin/env python
# coding:utf-8
# Purpose: 
# Created: 23.07.12
# Copyright (C) 2012, Manfred Moitzi
# License: GPLv3

__author__ = "mozman <mozman@gmx.at>"

import sys
import os
import time
import pprint
import dxfgrabber
from collections import Counter

sys.path.insert(0, os.path.abspath('..'))


def print_layers(counter):
    print("used Layers: {}".format(len(counter)))
    for item in sorted(counter.items()):
        print("Layer: {} has {} entities".format(*item))
        # pprint.pprint(item)


def main(filename):
    print("reading file: {}".format(filename))
    starttime = time.time()
    dxf = dxfgrabber.readfile(filename)
    endtime = time.time()
    print("time to read: {:.2f}s".format(endtime - starttime))
    print("entities: {:d}".format(len(dxf.entities)))
    print("defined Layers: {}".format(len(dxf.layers)))
    print_layers(Counter(entity.layer for entity in dxf.entities))
    for entity in dxf.entities:
        if entity.layer == "CUT":
            if isinstance(entity, dxfgrabber.dxfentities.Polyline):
                print("layer cut entity is close")
                pprint.pprint(entity.is_closed)
        if entity.layer == "14":
            if isinstance(entity, dxfgrabber.dxfentities.Polyline):
                print("layer 14 Polyline first vertex.")
                pprint.pprint(entity.vertices[0].location)
            if isinstance(entity, dxfgrabber.dxfentities.Line):
                print("layer 14 Line start")
                pprint.pprint(entity.start)
        if entity.layer == "SCRIBE":
            print("layer scribe")
            if isinstance(entity, dxfgrabber.dxfentities.Text):
                pprint.pprint(entity.text)
        if entity.layer == "TEXT":
            print("layer text")
            if isinstance(entity, dxfgrabber.dxfentities.Text):
                pprint.pprint(entity.text)


if __name__ == '__main__':
    # main(sys.argv[1])
    main(".\\testfiles\SA12145.DXF")
