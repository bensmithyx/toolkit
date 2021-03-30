#!/usr/bin/env python3
from subprocess import check_output #used to get ips valid on machine
import re #for regex when getting ip
import os #for outputting command line commands - for setting up listener at the end

class Colour:                    #class of all the colours we may use
    Black = "\u001b[30m"
    Red = "\u001b[31m"
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    White = "\u001b[37m"
    Cyan = "\u001b[36m"
    Reset = "\u001b[0m"
    # Theme
    Colour1 = Green
    Colour2 = Cyan
    Colour3 = Red
    Colour4 = White
    Text = Yellow

def display(text): #display in a format similar to other tools for prompt text
    print(f"\n{Colour.Blue}[{Colour.Red}+{Colour.Blue}]{Colour.Text} {text}{Colour.Reset}\n")

def displayerror(text): #display in similar format to display(text) but with x instead of + for an error
    print(f"\n{Colour.Blue}[{Colour.Black}x{Colour.Blue}]{Colour.Text} {text}{Colour.Reset}\n")

def get_scan_type():
    display("Which type of scan would you like to carry out?")
    scans = ["Light scan","Medium scan","Full scan","Custom scan"]
    for i in range(4):
        print(f"{Colour.Colour4}{i} - {Colour.Colour2}{scans[i]}{Colour.Reset}")
    try:
        scan = int(input(f"({Colour.Text}Scan Selection{Colour.Reset}) > "))
    except ValueError:
        displayerror("Error, please enter an integer value")
        return get_scan_type()
    else:
        if scan not in range(4):
            displayerror("Option entered not in correct range for scans, try again")
            return get_scan_type()
        return scan

def get_save():
    display("Would you like to save the scan to a file? (JSON format)")
    options = ["No","Yes"]
    for i in range(2):
        print(f"{Colour.Colour4}{i} - {Colour.Colour2}{options[i]}{Colour.Reset}")
    try:
        save = int(input(f"({Colour.Text}Save Selection{Colour.Reset}) > "))
    except ValueError:
        displayerror("Error, please enter an integer value")
        return get_save()
    else:
        if save not in range(2):
            displayerror("Option entered not in correct range, try again")
            return get_save()
        return save

def scan_save():
    display("Enter the name you want to save the file as")
    name = input(f"({Colour.Text}Filename Selection{Colour.Reset}) > ")
    return name+".json"

def scan_light():
    None

def scan_medium():
    None

def scan_full():
    None

def scan_custom():
    None



def main():
    scan = get_scan_type()
    save = get_save()
    filename = ""
    if save == 1:
        filename = scan_save()

if __name__=='__main__':
    main()