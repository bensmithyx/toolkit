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

def get_custom_options():
    options = []
    
    display("Which scan options would you like to include?")

    enter_options_again = True
    while enter_options_again == True:
        print(f"{Colour.Colour2}Enter the option numbers with a space in between each one, eg '2 5 7 10'{Colour.Reset}")
        
        options = ["Full scan","Targeted scan","Operating system information","Root cron jobs","Root processes"]
        for i in range(len(options)):
            print(f"{Colour.Colour4}{i} - {Colour.Colour2}{options[i]}{Colour.Reset}")
        
        user_input = " " + input(f"({Colour.Text}Option Selection{Colour.Reset}) > ") + " "
        for i in range(1, 21):
            if user_input.find(" " + str(i) + " ") != -1:
                options.append(i)

        print("Your scan: ", end=" ")
        for i in options:
            print(i, end=" ")
        print("\n")
    
        reenter_options = ""
        while reenter_options != "y" and reenter_options != "n":
            print("Are you happy with these options? Enter 'y' to continue or 'n' to try again:")
            reenter_options = input(" > ")
            if reenter_options == "y":
                enter_options_again = False
            elif reenter_options == "n":
                options = []
            else:
                displayerror("Invalid option, try again")
    
    return options    
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
    targeted_file_scan()
    	

def scan_medium():
    targeted_file_scan()


def scan_full():
    full_file_scan()


def scan_custom(scan_options):
    for i in scan_options:
    	scan(i)
    	

def scan(option_num):
    if option_num == 0:
    	# full file scan
    	display("Full file scan commencing...")
    	full_file_scan()
    	display("Full file scan completed")
    elif option_num == 1:
    	# targeted file scan
    	display("Targeted file scan commencing...")
    	targeted_file_scan()
    	display("Targeted file scan completed")
    elif option_num == 2:
    	display(" commencing...")
    elif option_num == 3:
    	display(" commencing...")
    elif option_num == 4:
    	display(" commencing...")
    elif option_num == 5:
    	display(" commencing...")
    elif option_num == 6:
    	display(" commencing...")
    elif option_num == 7:
    	display(" commencing...")
    elif option_num == 8:
    	display(" commencing...")
    elif option_num == 9:
    	display(" commencing...")
    elif option_num == 10:
    	display(" commencing...")
    elif option_num == 11:
    	display(" commencing...")
    elif option_num == 12:
    	display(" commencing...")

def full_file_scan():
    display(" commencing...")

def targeted_file_scan():
    display(" commencing...")	

def main():
    scan = get_scan_type()
    scan_options = []
    if scan == 3: #if it is a custom scan
    	scan_options = get_custom_options()
    	
    save = get_save()
    filename = ""
    if save == 1:
        filename = scan_save() #can you mess this up by typing in ../ or something?
    
    if scan == 0:
    	display("Light scan commencing...")
    	scan_light()
    elif scan == 1:
    	display("Medium scan commencing...")
    	scan_medium()
    elif scan == 2:
    	display("Full scan commencing...")
    	scan_full()
    else: # if scan == 3
    	display("Custom scan commencing...")
    	scan_custom(scan_options)
    
    display("The scan has been completed")


if __name__=='__main__':
    main()
