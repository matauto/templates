#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#########################################
#author: Mateusz O.
#repository: github.com/matauto/templates
#license: GPLv3
#########################################

import argparse
import sys
import os
from pathlib import Path
import shutil
import re
#from datetime import datetime

#parse input arguments
parser = argparse.ArgumentParser(
        prog = 'templates',
        description = 'Script help create files from templates',
        epilog = 'github.com/matauto/templates')
parser.add_argument("path",
                    default = "./",
                    type = Path,
                    help = "path to directory")
parser.add_argument("-n", "--name",
                    help = "target file name",
                   type = ascii)
parser.add_argument("-t", "--template",
                    help = "source template name",
                    type = ascii)

#global variables
args = parser.parse_args()
scriptDir = sys.path[0]
pathDir = Path(args.path)
gLongScreenLine = "------------------------------------------------------------"
gSpecialFiles = ['description.txt', 'postBash.sh', 'postPython.py']

def clear_screen():
    #\033[ is Control Sequence Introducer.
    print("\033[H\033[2J", end = '')

def validateInput(regExp, lowNo, highNo, usrIn):
    if (lowNo != 0 or highNo != 0) and re.match("^[0-9]+$", usrIn):
        if int(usrIn) >= lowNo and int(usrIn) <= highNo:
            return usrIn
        else:
            print("wrong number")
            return "errUserEntry"
    elif re.match(regExp, usrIn):
        return usrIn
    elif usrIn == "q":
        return "q"
    else:
        print("wrong input")
        return "errUserEntry"

def get_folder_list(pathToFolder, doPrint):
    n = 1
    if doPrint:
        print(pathToFolder)
    listOfFolders = []
    for root, folder, files in os.walk(pathToFolder):
        if n == 1:
            for item in folder:
                if doPrint:
                    print(n,"\t",item)
                listOfFolders.append(item)
                n = n + 1
    return listOfFolders

def get_files_list(pathToFolder, doPrint):
    specialFiles = gSpecialFiles
    n = 1
    if doPrint:
        print(pathToFolder)
    listOfFiles = []
    for root, folder, files in os.walk(pathToFolder):
        if n == 1:
            for item in files:
                if not (item in specialFiles):
                    if doPrint:
                        print(n,"\t",item)
                    listOfFiles.append(item)
                    n = n + 1
    return listOfFiles

def process_file(sourcePath, targetPath):
    if os.path.isfile(sourcePath):
        print(gLongScreenLine)
        print("Edit file: " + targetPath)
        print(gLongScreenLine)
        
        with open(sourcePath,'r') as sourceFile, open(targetPath, 'a') as targetFile:
            for line in sourceFile:
                matchTag = re.search(r"(<<<(.*?)>>>)", line)
                if matchTag:
                    print(line, end='')
                    print(gLongScreenLine)
                    userInput = input("Replace " + matchTag.group() + ": ")
                    line = re.sub(matchTag.group(), userInput, line)
                    targetFile.write(line)
                    print(gLongScreenLine)
                else:
                    targetFile.write(line)
                    print(line, end='')
    else:
        print("sourcePath is not file")
        print(sourcePath)

def print_menu(menuOpt):
    regExp = "{q}"
    lowNo = 0
    highNo = 0
    print(gLongScreenLine)
    match menuOpt:
        case 'start':
            clear_screen()
            print("TEMPLATES")
            print("github.com/matauto/templates")
            print(gLongScreenLine)
            print("Choose what you want to do:")
            print("1 Create new project.")
            print("2 Create new files.")
            lowNo = 1
            highNo = 2
            print("\nType 'q' to quit")
            print(gLongScreenLine)
        case 'project':
            clear_screen()
            print("NEW PROJECT")
            print(gLongScreenLine)
            pathNewProject = scriptDir + "/NEW_PROJECT"
            listOfFolders = get_folder_list(pathNewProject, 1)
            if listOfFolders:
                lowNo = 1
                highNo = len(listOfFolders)
            else:
                lowNo = 0
                highNo = 0
            print("\nType 'q' to quit")
            print(gLongScreenLine)
        case 'file':
            clear_screen()
            print("NEW FILE")
            print(gLongScreenLine)
            pathNewProject = scriptDir + "/NEW_FILES"
            listOfFolders = get_folder_list(pathNewProject, 1)
            if listOfFolders:
                lowNo = 1
                highNo = len(listOfFolders)
            else:
                lowNo = 0
                highNo = 0
            print("\nType 'q' to quit")
            print(gLongScreenLine)
        case 'get_name':
            print("Enter the new name for file")
            print(gLongScreenLine)
            lowNo = 0
            highNo = 0
            regExp = "^\w+$"
        case _:
            print("unspecified menu entry")
   
    userValidated = "errUserEntry"
    while (userValidated == "errUserEntry"):
        userInput = input("User input: ")
        userValidated = validateInput(regExp, lowNo, highNo, userInput)
    
    return userValidated

def main():
    if (pathDir.exists() and pathDir.is_dir()):
        userInput = print_menu('start')
        if userInput == "1":
            userInput = print_menu('project')
            listOfFolders = get_folder_list((scriptDir + "/NEW_PROJECT"), 0)
            if listOfFolders:
                newProjectDir = scriptDir + "/NEW_PROJECT/" + listOfFolders[int(userInput)-1]
                print(newProjectDir)
        elif userInput == "2":
            userInput = print_menu('file')
            clear_screen()
            listOfFolders = get_folder_list((scriptDir + "/NEW_FILES"), 0)
            if listOfFolders:
                newFileDir = scriptDir + "/NEW_FILES/" + listOfFolders[int(userInput)-1] + "/"
                listOfFiles = get_files_list(newFileDir, 1)
                for file in listOfFiles:
                    print("\n")
                    print(file)
                    userInput = print_menu('get_name')
                    targetPath = pathDir.absolute().as_posix() + "/" + userInput
                    fileExt = re.search("\.\w+$", file)
                    if fileExt:
                        targetPath = targetPath + fileExt.group()
                    clear_screen()
                    process_file(newFileDir + file, targetPath)
        else:
            print("error")
    else:
        print("path is not directory")

if __name__ == "__main__":
    main()
