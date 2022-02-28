from black import out
from prompt_toolkit.shortcuts import input_dialog, message_dialog, button_dialog

def main():
    # Elements
    #   string path of input
    #   string path out output root folder
    #   name path of output root folder

    # Metadata to sort by
    #   Date (Day)      /YYYY/MM/DD
    #   Date (Month)    /YYYY/MM
    #   Date(Year)      /YYYY

    # Logic Flow - later on make it so that I could also just call directly from the command line

    instr = input()
    outstr = output()
    nameout = outname()


def input():
    instr = input_dialog(title='autosort CLI', text='Path of input:').run()
    if instr == "":
        input()
    else:
        return instr

def output():
    outstr = input_dialog(title='autosort CLI', text='Path of output:').run()
    if outstr == "":
        output()
    else:
        return outstr

def outname():
    name = input_dialog(title='autosort CLI', text='Name of output folder:').run()
    if name == "":
        outname()
    else:
        return name

def confirm(instr, outstr, nameout):
    return button_dialog(title='autosort CLI',text='Confirm:\nInput folder:'+instr+'\nOutput folder:'+outstr+'\nName of output folder:'+nameout+'\nIs this information correct?', buttons=[('Yes', True),('No', False),('Cancel',None)])

def genericmessage(astring):
    message_dialog(title='autosort CLI', text=astring+'\nPress ENTER to quit.').run()

if __name__ == "__main__":
    main()
