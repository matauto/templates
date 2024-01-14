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
import subprocess
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
gAutoFillFile = scriptDir + '/autoFillTag.conf'

def clear_screen():
    #\033[ is Control Sequence Introducer.
    print("\033[H\033[2J", end = '')

def color_text(orgText, colorName):
    resetCode = "\033[0m"
    if colorName == "red":
        colorCode = "\033[31m"
    elif colorName == "green":
        colorCode = "\033[32m"
    elif colorName == "yellow":
        colorCode = "\033[33m"
    elif colorName == "blue":
        colorCode = "\033[34m"
    else:
        return orgText

    coloredText = colorCode + str(orgText) + resetCode
    return coloredText

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
                    print(color_text(n, "red"),"\t",item)
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
                        print(color_text(n, "red"),"\t",item)
                    listOfFiles.append(item)
                    n = n + 1
    return listOfFiles

def display_description_file(pathToDir):
    specialFiles = gSpecialFiles
    for item in specialFiles:
        if re.match(".+\.txt$", item):
            with open(pathToDir + item) as file:
                for line in file:
                    print(line, end='')
                print("")

def fill_specialTag(tagName, filePath):
    specialTagsList = ['<<<test>>>', '<<<(fileName)([0-9]+)>>>', '<<<>>>', '<<<(filePath)>>>']
    for specialTag in specialTagsList:
        searchResult = re.search(specialTag, tagName)
        if searchResult:
            tagSpec = searchResult.group()
            if tagSpec == "<<<>>>":
                return ""
            elif tagSpec[3:6] == "fil": 
                if searchResult.group(1) == "filePath":
                    return filePath
                elif searchResult.group(1) == "fileName":
                    fileNameRe = re.search(r"(.+?)\/(\w+?\.?\w+)$", filePath)
                    if fileNameRe:
                        return fileNameRe.group(2)
                    else:
                        print("fill_specialTag: fileNameRe do not found")
            else:
                print(tagSpec)
    return ""

def auto_fill_tag(tagName, filePath):
    spTagResult = fill_specialTag(tagName, filePath)
    if spTagResult != "":
        return spTagResult

    configFile = gAutoFillFile
    with open(configFile,'r') as tagFile:
        for line in tagFile:
            matchTag = re.search(r"(^<<<.*?>>>)=(.*?$)", line)
            if matchTag:
                if matchTag.group(1) == tagName:
                    #print("Empty, replaced with: ", end='')
                    searchResult = re.search(r"(!cmd:)(.*?$)", matchTag.group(2))
                    if searchResult:
                        #print(searchResult.group(2))
                        commandResult = subprocess.check_output([searchResult.group(2)], shell=True)
                        cmdRes2 = re.search(r"b'(.*?)\\n'", str(commandResult))
                        if cmdRes2:
                            commandResult = cmdRes2.group(1)
                        #print(cmdRes2.group(1))
                        #print(str(commandResult))
                        return str(commandResult)
                    else:
                        #print(matchTag.group(2))
                        return matchTag.group(2)
    #print("Tag not listed in auto fill config file")
    return ""

def process_file(sourcePath, targetPath):
    if os.path.isfile(sourcePath):
        print(color_text(gLongScreenLine, "green"))
        print(color_text("Edit file: " + targetPath, "green"))
        print(color_text(gLongScreenLine, "green"))
        
        with open(sourcePath,'r') as sourceFile, open(targetPath, 'a') as targetFile:
            for line in sourceFile:
                matchTag = re.search(r"(<<<(.*?)>>>)", line)
                if matchTag:
                    print(line, end='')
                    print(color_text(gLongScreenLine, "green"))
                    autoFill = auto_fill_tag(matchTag.group(), targetPath)
                    if autoFill:
                        print(color_text("Press enter to autoFill: ", "green"), end='')
                        print(color_text(autoFill, "green"))
                    userInput = input(color_text("Replace " + matchTag.group() + ": ", "green"))
                    if userInput == "" and autoFill:
                        userInput = autoFill
                    line = re.sub(matchTag.group(), userInput, line)
                    targetFile.write(line)
                    print(color_text(gLongScreenLine, "green"))
                else:
                    targetFile.write(line)
                    print(line, end='')
    else:
        print("sourcePath is not file")
        print(color_text(sourcePath, "red"))

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
            print(color_text("1 ", "red") + "Create new project.")
            print(color_text("2 ", "red") + "Create new files.")
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
                display_description_file(newFileDir)
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
        print(color_text("path is not directory", "red"))

if __name__ == "__main__":
    main()
