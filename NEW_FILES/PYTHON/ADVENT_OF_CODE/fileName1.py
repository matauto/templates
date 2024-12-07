#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: <<<AUTHOR>>>
#Date:<<<DATE>>>
#Time:<<<TIME>>>
#based on Advent Of Code template from github.com/matauto/templates

import argparse
import sys
import os
import re
from pathlib import Path

parser = argparse.ArgumentParser(
        prog = '<<<fileName1>>>',
        description = 'advent of code problem solver',
        epilog = 'none')
parser.add_argument("file",
                    default = ".",
                    type = Path,
                    help = "input file for script")
parser.add_argument("part",
                    default = "0",
                    type = int,
                    help = "input file for script")
args = parser.parse_args()

def main():
    fileName=Path(args.file)
    partExec=args.part
    if (fileName.exists() and fileName.is_file()):
        if partExec==0 or partExec==1:
            #solution for first part of puzzle
            print("PART ONE")
            result=0
            inputFile = open(fileName, 'r', encoding="utf-8")
            for line in inputFile:

            print("Part one answear: ", result)

        if partExec==0 or partExec==2:
            #solution for second part of puzzle 
            print("PART TWO")

            print("Part two answear: ", result)
    else:
        print("it is not file")

if __name__ == "__main__":
    main()
