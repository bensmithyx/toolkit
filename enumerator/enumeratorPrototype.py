#!/usr/bin/env python3
from subprocess import check_output #used to get ips valid on machine
import re #for regex when getting ip
import os #for outputting command line commands - for setting up listener at the end

def get_scan_type():
    print("Which type of scan would you like to carry out?")
    scans = ["Custom scan","Light scan","Medium scan","Full scan"]
    for i in range(4):
        print(f"{i} - {scans[i]}")
    try:
        scan = int(input("(Scan Selection) > "))
    except ValueError:
        print("Error: please enter an integer value")
        return get_scan_type()
    else:
        if scan not in range(4):
            print("Option entered not in correct range, try again")
            return get_scan_type()
        return scan

def get_custom_options():
    options = []
    
    enter_options_again = True
    while enter_options_again == True:
        # Asks the user which scan options they want in their custom scan, showing the user which scan options correlate to which scan number.
        print("Which scan options would you like to include?")
        print("Enter the option numbers with a space between each one, eg '2 7 16'")
        option_list = ["System information","Device information","Process information","Network information","User information","Software information","File scan"]
        for i in range(len(option_list)):
            print(f"{i} - {option_list[i]}")
    
        # gets the scan options that the user wants by searching the user input for each of the scan option numbers and placing them into their own list. This means that the option numbers are now stored in the correct order and duplicates are eliminated.
        user_input = " " + input("(Option Selection) > ") + " "
        for i in range(len(option_list)):
            if user_input.find(" " + str(i) + " ") != -1:
                options.append(i)
    
        # shows the user what the computer has interpreted as their scan from their input.
        print("\nYour scan: ", end=" ")
        for i in options:
            if i != options[len(options) - 1]:
                print(option_list[i], end=", ")
            else:
                print(f"{option_list[i]}")
    
        # asks the user if they are happy with these options, or if they want to try chosing their options again
        reenter_options = ""
        while reenter_options != "1" and reenter_options != "0":
            print("Are you happy with the options you have selected?")
            options = ["No","Yes"]
            for i in range(2):
                print(f"{i} - {options[i]}")

            reenter_options = input("(Option Confirmation) > ")
            if reenter_options == "1":
                return options
            elif reenter_options == "0":
                options = []
            else:
                print("Invalid option, try again")
             
def get_save():
    print("Would you like to save the scan to a file? (JSON format)")
    options = ["No","Yes"]
    for i in range(2):
        print(f"{i} - {options[i]}")
    try:
        save = int(input(f"(Save Selection) > "))
    except ValueError:
        print("Error, please enter an integer value")
        return get_save()
    else:
        if save not in range(2):
            print("Option entered not in correct range, try again")
            return get_save()
        return save

def scan_save():
    print("Enter the name you want to save the file as")
    name = input("(Filename Selection) > ")
    return name+".json"

def scan_light():
    light_scan_options = [0,1]
    for i in light_scan_options:
        scan(i)

def scan_medium():
    medium_scan_options = [0,1,2,3]
    for i in medium_scan_options:
        scan(i)

def scan_full():
    full_scan_options = [0,1,2,3,4,5]
    for i in full_scan_options:
        scan(i)

def scan_custom(scan_options):
    for i in scan_options:
      	scan(i)

def title(name):
    os.system('echo ')
    os.system('%s %s %s' % ("echo '########## ", str(name), " ##########'"))
    os.system('echo ')

def scan(option_num):
    if option_num == 0: # OS information
        title("OS INFORMATION")
        os.system('(cat /proc/version || uname -a ) 2>/dev/null; lsb_release -a 2>/dev/null')
    elif option_num == 1: # SUDO version
        title("SUDO VERSION")    
        os.system('sudo -V 2>/dev/null')
    elif option_num == 2: # Environment variables information
    	  title("ENVIRONMENT VARIABLES INFORMATION")
        os.system('(env || set) 2>/dev/null')
    elif option_num == 3: # Current user information
    	  title("CURRENT USER INFORMATION")    
        os.system('id || (whoami && groups) 2>/dev/null')
    elif option_num == 4: # All user information
    	  title("INFORMATION ON ALL USERS")    
        os.system('cat /etc/passwd | cut -d: -f1; cat /etc/passwd | grep "sh$"; awk -F: '($3 == "0") {print}' /etc/passwd; w; last | tail; lastlog; for i in $(cut -d":" -f1 /etc/passwd 2>/dev/null);do id $i;done 2>/dev/null | sort')
    elif option_num == 5: # Network information
    	  title("NETWORK INFORMATION")    
        os.system('(ip addr show || ifconfig) 2>/dev/null; (ss -auntp || netstat -auntp) 2>/dev/null; (route -n || ip route show) 2>/dev/null; (arp -n || ip neigh show) 2>/dev/null')

def main():
    scan = get_scan_type()
    scan_options = []
    if scan == 0: #if it is a custom scan
    	scan_options = get_custom_options()
    	
    save = get_save()
    filename = ""
    if save == 1:
        filename = scan_save() #can you mess this up by typing in ../ or something?
    
    if scan == 0:
        print("Custom scan commencing...")
        scan_custom(scan_options)
    elif scan == 1:
      	print("Light scan commencing...")
      	scan_light()
    elif scan == 2:
    	  print("Medium scan commencing...")
    	  scan_medium()
    else: # if scan == 3
    	  print("Full scan commencing...")
    	  scan_full()
    
    print("The scan has been completed")


if __name__=='__main__':
    main()
