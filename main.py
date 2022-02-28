from unicodedata import name
from prompt_toolkit.shortcuts import (
    input_dialog,
    message_dialog,
    button_dialog,
    radiolist_dialog,
)
import os
import shutil


def main():
    # Logic Flow - later on make it so that I could also just call directly from the command line

    instr = input()
    verify(instr)
    outstr = output()
    verify(outstr)
    nameout = outname()
    if nameout == "":
        nameout = None
    outpath = outstr + nameout
    method = choosemethod()
    confirm(instr, outstr, nameout, method)
    # ! Add an option for copy vs move and to only copy files with a certain file extension
    sort(instr, outpath, method)


def sort(instr, outpath, method):
    """Sorts the input directory into the output directory via the defined sort method"""
    os.mkdir(outpath)
    traversedir(instr, outpath, method)


def traversedir(path, outpath, method):
    """Traverses the input directory recursively until it finds a file. Then calls separate methods for in and out paths and copying."""
    if os.path.isdir(path):
        for filename in os.listdir(path):
            f = os.path.join(path, filename)
            if os.path.isdir(f):
                traversedir(f)
            elif os.path.isfile(f):
                copy(f, outpath, method)


def copy(filepath, outpath, method):
    """Handles days only"""
    time = time.ctime(os.path.getctime(filepath)).split()
    if method == "Day":
        dest = outpath + "/" + time[-1] + "/" + time[1] + "/" + time[2] + "/"
    elif method == "Month":
        dest = outpath + "/" + time[-1] + "/" + time[1] + "/"
    elif method == "Year":
        dest = outpath + "/" + time[-1] + "/"
    # TODO Add some more sort methods here
    if os.path.isdir():
        #! Need to handle filenotfound exception
        shutil.copy2(filepath, dest)
    else:
        os.mkdir(dest)
        shutil.copy2(filepath, dest)


def input():
    """Queries the user for the input directory"""
    instr = input_dialog(title="autosort CLI", text="Path of input:").run()
    if instr == "":
        input()
    else:
        return instr


def output():
    """Queries the user for the output parent directory"""
    outstr = input_dialog(title="autosort CLI", text="Path of output:").run()
    if outstr == "":
        output()
    else:
        return outstr


def outname():
    """Queries the user for the output folder name"""
    name = input_dialog(title="autosort CLI", text="Name of output folder:").run()
    if name == "":
        outname()
    else:
        return name


def choosemethod():
    """Prompts the user for the sort method to be used"""
    result = radiolist_dialog(
        title="autosort CLI",
        text="Sort method:\n[Press space to select]",
        values=[("Day", "/YYYY/MM/DD/"), ("Month", "/YYYY/MM/"), ("Year", "/YYYY/")],
    ).run()
    return result


def confirm(instr, outstr, nameout, method):
    """Queries the user to confirm the validity of their data"""
    out = button_dialog(
        title="autosort CLI",
        text="Confirm:\nInput folder:"
        + instr
        + "\nOutput folder:"
        + outstr
        + "\nName of output folder:"
        + instr
        + "/"
        + nameout
        + "\nMethod:"
        + method
        + "\nIs this information correct?",
        buttons=[("Yes", True), ("No", False), ("Cancel", None)],
    ).run()
    return out


def verify(checkstr):
    """Exits the program if the string is none"""
    if checkstr == None:
        exit()


def genericmessage(astring):
    """Generates a generic message based on astring"""
    message_dialog(title="autosort CLI", text=astring + "\nPress ENTER to quit.").run()


if __name__ == "__main__":
    main()
