#!/usr/bin/env python

from prompt_toolkit.shortcuts import (
    input_dialog,
    message_dialog,
    button_dialog,
    radiolist_dialog,
    ProgressBar,
    checkboxlist_dialog,
)
import os
import shutil
import time
import click
from yaspin import yaspin


TITLE = "filesort CLI v0.1.4"


@click.command()
def cli():
    """Primary entry point for GUI operations"""
    additional = None

    # Takes input from the user and formats it
    instr = input()
    verify(instr)
    outstr = output()
    verify(outstr)
    nameout = outname()
    if nameout == None:
        exit()
    elif nameout == "":
        nameout = None
    outpath = os.path.join(outstr, nameout)
    method = choosemethod()
    if method == None:
        exit()

    # Asks the user to confirm their choice
    out = confirm(instr, outstr, nameout, method)
    if out == None:
        exit()
    elif out == False:
        cli()
    elif out == 1:
        additional = adds()
        # ! ROUTE THROUGH CONFIRM AGAIN
        if "ext" in additional:
            extension = promptextension()
            sort(instr, outpath, method, additional, extension)
        else:
            sort(instr, outpath, method, additional)

    # Sort with no additional options specified
    else:
        # ! Add an option for copy vs move and to only copy files with a certain file extension
        sort(instr, outpath, method)
        genericmessage("Sort complete!")


#! I should probably change this next line and permit verbose operation
@click.option("-v", "--version", "version")
def version(TITLE):
    """Prints the version"""
    click.echo(TITLE)


@click.option("-d", "--day", "sort by day", type=(str, str))
def termday(day):
    instr, outpath = day
    if instr == None or instr == "" or outpath == None or outpath == "":
        click.echo(
            "Please input the input string followed by a space, then your output path that contains a new destination folder"
        )
        exit()
    else:
        sort(instr, outpath, "Day")


@click.option("-m", "--month", "sort by month", type=(str, str))
def termmonth(month):
    instr, outpath = month
    if instr == None or instr == "" or outpath == None or outpath == "":
        click.echo(
            "Please input the input string followed by a space, then your output path that contains a new destination folder"
        )
        exit()
    else:
        sort(instr, outpath, "Month")


@click.option("-y", "--year", "sort by year", type=(str, str))
def termyear(year):
    instr, outpath = year
    if instr == None or instr == "" or outpath == None or outpath == "":
        click.echo(
            "Please input the input string followed by a space, then your output path that contains a new destination folder"
        )
        exit()
    else:
        sort(instr, outpath, "Year")


@click.option("-e", "--extension", "sort by file extension", type=(str, str))
def termextension(extension):
    instr, outpath = extension
    if instr == None or instr == "" or outpath == None or outpath == "":
        click.echo(
            "Please input the input string followed by a space, then your output path that contains a new destination folder"
        )
        exit()
    else:
        sort(instr, outpath, "File extension")


def sort(instr, outpath, method, additional, extension):
    """Sorts the input directory into the output directory via the defined sort method"""
    # TODO This can probably be removed for simplicity
    os.mkdir(outpath)
    traversedir(instr, outpath, method, additional, extension)


def traversedir(path, outpath, method, additional, extension):
    """Traverses the input directory recursively until it finds a file. Then calls separate methods for in and out paths and copying."""
    if os.path.isdir(path):
        with yaspin(text="Moving files..."):
            for filename in os.listdir(path):
                f = os.path.join(path, filename)
                if additional != None:
                    if "ext" in additional and extension != None:
                        if f.endswith(extension):
                            if os.path.isdir(f):
                                traversedir(f, outpath, method, extension)
                            elif os.path.isfile(f):
                                copy(f, outpath, method)
                    elif "sym" in additional:
                        if os.path.islink(f):
                            if "v" in additional:
                                print("Skipping symlink " + f)
                            else:
                                pass
                else:
                    if os.path.isdir(f):
                        traversedir(f, outpath, method)
                    elif os.path.isfile(f):
                        copy(f, outpath, method)


def copy(filepath, outpath, method, additional):
    """Main copy method"""
    if method == "Day" or method == "Month" or method == "Year":
        ctime = time.ctime(os.path.getctime(filepath)).split()
        if method == "Day":
            dest = os.path.join(outpath, ctime[-1], ctime[1], ctime[2])
        elif method == "Month":
            dest = os.path.join(outpath, ctime[-1], ctime[1])
        elif method == "Year":
            dest = os.path.join(outpath, ctime[-1])
    elif method == "File extension":
        dest = outpath + "/" + os.path.splitext(filepath)[1].replace(".", "")
    try:
        if os.path.isdir(dest):
            shutil.copy2(filepath, dest)

        else:
            os.makedirs(dest)
            shutil.copy2(filepath, dest)
        if additional != None:
            if "v" in additional:
                click.echo("Copied" + filepath + " to " + dest)
    except PermissionError as p:
        # click.echo(p)
        click.echo(
            "You do not have permission to access the following file: " + filepath
        )
    except NotADirectoryError as n:
        # click.echo(n)
        click.echo("Error copying " + filepath)


def input():
    """Queries the user for t/home/vivi/Documents/testing/outdirhe input directory"""
    instr = input_dialog(title=TITLE, text="Path of input:").run()
    if instr == "":
        input()
    else:
        return instr


def output():
    """Queries the user for the output parent directory"""
    outstr = input_dialog(title=TITLE, text="Path of output:").run()
    if outstr == "":
        output()
    else:
        return outstr


def outname():
    """Queries the user for the output folder name"""
    name = input_dialog(title=TITLE, text="Name of output folder:").run()
    if name == "":
        outname()
    else:
        return name


def choosemethod():
    """Prompts the user for the sort method to be used"""
    result = radiolist_dialog(
        title=TITLE,
        text="Sort method:\n[Press space to select]",
        values=[
            ("Day", "/YYYY/MM/DD/"),
            ("Month", "/YYYY/MM/"),
            ("Year", "/YYYY/"),
            ("File extension", "/xxx/ (File extension)"),
        ],
    ).run()
    return result


def adds():
    """Gives the user a choice of additional options to execute"""
    result = checkboxlist_dialog(
        title=TITLE,
        text="Additional options:\n[Press space to select]",
        values=[
            ("v", "Verbose"),
            ("ext", "Specify an extension to copy"),
            ("sym", "Ignore symlinks"),
        ],
    ).run()
    return result


def promptextension():
    """Queries the user for the file extension"""
    name = input_dialog(title=TITLE, text="File extension:").run()
    if name == "":
        promptextension()
    else:
        return name


def confirm(instr, outstr, nameout, method):
    """Queries the user to confirm the validity of their data"""
    out = button_dialog(
        title=TITLE,
        text="Confirm:\nInput folder: "
        + instr
        + "\nOutput folder: "
        + outstr
        + "\nName of output folder: "
        + instr
        + "/"
        + nameout
        + "\nMethod: "
        + method
        + "\nIs this information correct?",
        buttons=[
            ("Yes", True),
            ("No", False),
            ("Additional Options", 1),
            ("Cancel", None),
        ],
    ).run()
    return out


def verify(checkstr):
    """Exits the program if the string is none"""
    if checkstr == None:
        exit()


def genericmessage(astring):
    """Generates a generic message based on astring"""
    message_dialog(title=TITLE, text=astring + "\nPress ENTER to quit.").run()


if __name__ == "__main__":
    cli()
