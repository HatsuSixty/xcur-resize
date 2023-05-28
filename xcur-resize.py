#!/bin/env python3

from os import getenv, walk
from os.path import isfile, islink, join as pjoin
from subprocess import run
from sys import argv, stdout, stderr
from shlex import join as sjoin

def assert_executable_exists(exe):
    found = False
    for p in getenv("PATH").split(":"):
        if isfile(pjoin(p, exe)):
            found = True
            break
    if not found:
        print(f"ERROR: Could not find `{exe}` in $PATH", file=stderr)
        exit(1)

def run_cmd(cmd):
    print(f"[CMD] {sjoin(cmd)}")
    run(cmd)

def run_command_in_files_with_extension(ext, command: str, folder):
    for d, fol, fil in walk(folder):
        for f in fil:
            fpath = pjoin(d, f)
            if (not islink(fpath)) and fpath.endswith(ext):
                run_cmd(["sh", "-c", command.replace("<f>", fpath)])

def usage(err):
    stream = stdout if err else stderr
    print("USAGE: xcur-resize.py <FOLDER> [GEOMETRY]", file=stream)
    print("  FOLDER: The folder containing cursor files. If `help` is specified instead, this help is printed", file=stream)
    print("  GEOMETRY: ImageMagick geometry to get applied in FOLDER's files", file=stream)

if len(argv) < 2:
    print("ERROR: No argument was provided")
    usage(True)
    exit(1)

if argv[1] == "help":
    usage(False)
    exit(0)

geometry = "75%"
if len(argv) > 2:
    geometry = argv[2]

assert_executable_exists("mogrify")
assert_executable_exists("xcur2png")
assert_executable_exists("xcursorgen")

cursors = argv[1]

run_command_in_files_with_extension("",
                                    f"""if [ $(file <f> | awk '{{ print $2 }}') = \"X11\" ]; then \\
                                      xcur2png -d {cursors} -c \"<f>.conf\" \"<f>\"; \\
                                    fi""",
                                    cursors)
run_command_in_files_with_extension(".png", f"mogrify -resize {geometry} \"<f>\"", cursors)
run_command_in_files_with_extension(".conf",
                                    f"xcursorgen \"<f>\" $(dirname '<f>')/$(basename '<f>' .conf) -p \"{cursors}\"",
                                    cursors)
