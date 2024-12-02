#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: <<<AUTHOR>>>
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
args = parser.parse_args()

def main():
    fileName=Path(args.file)
    if (fileName.exists() and fileName.is_file()):
        inputFile = open(fileName, 'r', encoding="utf-8")

        print("PART ONE")
        #solution for first part of puzzle
        for line in inputFile:

        #calculate result
        result=0

        print("Part one answear: ", result)

        print("PART TWO")
        #solution for second part of puzzle 

        print("Part two answear: ", result2)
    else:
        print("it is not file")

if __name__ == "__main__":
    main()
