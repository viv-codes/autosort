from prompt_toolkit.shortcuts import (
    input_dialog,
    message_dialog,
    button_dialog,
    radiolist_dialog,
)


def main():
    # Elements
    #   string path of input
    #   string path out output root folder
    #   name path of output root folder

    # Logic Flow - later on make it so that I could also just call directly from the command line

    instr = input()
    verify(instr)
    outstr = output()
    verify(outstr)
    nameout = outname()
    if nameout == "":
        nameout = None
    method = choosemethod()
    confirm(instr, outstr, nameout, method)
    # sort(instr, outstr+nameout)


def choosemethod():
    result = radiolist_dialog(
        title="autosort CLI",
        text="Sort method:\n[Press space to select]",
        values=[("Day", "/YYYY/MM/DD/"), ("Month", "/YYYY/MM/"), ("Year", "/YYYY/")],
    ).run()
    return result


# def sort(instr, outpath)


def input():
    instr = input_dialog(title="autosort CLI", text="Path of input:").run()
    if instr == "":
        input()
    else:
        return instr


def output():
    outstr = input_dialog(title="autosort CLI", text="Path of output:").run()
    if outstr == "":
        output()
    else:
        return outstr


def outname():
    name = input_dialog(title="autosort CLI", text="Name of output folder:").run()
    if name == "":
        outname()
    else:
        return name


def confirm(instr, outstr, nameout, method):
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
    if checkstr == None:
        exit()


def genericmessage(astring):
    message_dialog(title="autosort CLI", text=astring + "\nPress ENTER to quit.").run()


if __name__ == "__main__":
    main()
