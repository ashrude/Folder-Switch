#!/usr/bin/python3
import os
from zipfile import ZipFile
import sys

extension = (".switch.c", ".switch")
dir = os.getcwd()
filename = "switch.py"

def list_dir():
    dirlist = [dir]
    files = []
    list = []
    while len(dirlist) > 0:
        for (dirpath, dirnames, filenames) in os.walk(dirlist.pop()):
            dirlist.extend(dirnames)
            files.extend(map(lambda n: os.path.join(*n), zip([dirpath] * len(filenames), filenames)))
    for file in files:
        list.append((file[:len(dir)]).replace(" ", "\ "))
    return files

def parse_dir(full_dir):
    list = [[], [], ""]
    if full_dir == True:
        files = list_dir() 
    else:
         files = os.listdir(dir)
    for x in files:
        if x.find(extension[0]) != -1:
            list[2] = x
        if x.find(extension[0]) == -1 and x.find(extension[1]) != -1:
            list[1].append(x)
        if x.find(extension[0]) == -1 and x.find(extension[1]) == -1:
            list[0].append(x)
    for x in list[0]:
        if x == filename: list[0].remove(filename)
    return list

def unzip(target):
    f=open(target.replace(extension[1], extension[0]), "x")
    f.write("")
    f.close()
    with ZipFile(target, "r") as zip:
        zip.extractall(dir)
    os.remove(target)


def mkzip():
    target_files, target = parse_dir(True)[0], parse_dir(True)[2]
    if target != "":
        os.remove(target)
        with ZipFile(target.replace(extension[0], extension[1]), "w") as zip:
            for file in target_files:
                zip.write(file)
        for file in target_files:
            os.remove(file)
    else:
        pass

def swap(target):
    mkzip()
    unzip(target)

def list_branches(numbers):
    options = parse_dir(False)[1]
    i=0
    string = ""
    while i < len(options):
        if numbers == True:
            string += f"{i}: {(options[i])[:-(len(extension[1]))]}"
        else:
            string += f"{(options[i])[:-(len(extension[1]))]}"
        string += "\n"
        i+=1
    return string

def check(input):
    options = parse_dir(False)[1]
    i=0
    while i < len(options):
        if options[i].replace(extension[1], "") == input:
            return options[i]
        elif options[i] == input:
            return options[i]
        i+=1
    return ""
#### user level functions ####

def switch():
    if len(parse_dir(False)[1]) == 0: 
        help("It seems there are no branches created in this directory!")
        sys.exit()
    print(list_branches(True))
    swap((parse_dir(True)[1])[int(input("enter selection: "))])

def help(error):
    print(f"{error}\n")
    print(f"[--help] for information on how to use {filename}\n[--create] Creates new branch\n[--close] Closes any open branch\n[--list] Lists all branches\n[--open] Opens a branch without closing the last one\n[<branch name>] Swaps to specified branch")

def create():
    mkzip()
    if len(sys.argv) == 3:
        new_name = sys.argv[2]
    else:
        new_name = input("What would you like to call this branch? \n")
    f=open(f"{new_name}{extension[0]}", "x")
    f.write("")
    f.close()

#### function calls ####

if len(sys.argv) == 1:
    switch()
elif sys.argv[1] == "-h" or sys.argv[1] == "--help" or sys.argv[1] == "help":
    help("")
elif sys.argv[1] == "--create":
    create()
elif sys.argv[1] == "--close":
    mkzip()
elif sys.argv[1] == "--list":
    print(list_branches(False))
elif sys.argv[1] == "--open":
    unzip(sys.argv[2])
else:
    swap(check(sys.argv[1])) if check(sys.argv[1]) != "" else help("no file with that filename was found!")
