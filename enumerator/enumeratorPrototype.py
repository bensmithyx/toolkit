#!/usr/bin/env python3
from subprocess import check_output #used to get ips valid on machine
import re #for regex when getting ip
import os #for outputting command line commands - for setting up listener at the end

def get_scan_type():
    print("Enter 0 for a custom scan or 1 for a full scan")
    try:
        scan = int(input(" > "))
    except ValueError:
        print("ERROR: PLEASE ENTER AN INTEGER")
        return get_scan_type()
    else:
        if scan != 0 and scan != 1:
            print("ERROR: PLEASE NETER A VALID OPTION")
            return get_scan_type()
        else:
            return scan

def get_custom_options():
    options = []
    
    # Asks the user which scan options they want in their custom scan, showing the user which scan options correlate to which scan number.
    print("Which scan options would you like to include?")
    print("Enter the option number one at a time, entering '-1' when you are done")
    option_list = ["OS information","SUDO version","Environment variable information","Defences information","DMESG signature information"]
    for i in range(len(option_list)):
        print(f"{i} - {option_list[i]}")

    # gets the scan options that the user wants and places them into an array
    user_input = 1
    while user_input != -1:
        user_input = int(input(" > "))
        if user_input >= 0 and user_input <= 4:
            options.append(user_input)
        elif user_input == -1:
            print("Options choices submitted!")
        else:
            print("Error: invalid option selected!")
        
    return options
             
def get_save():
    print("Would you like to save the scan to a file?")
    print("Enter 1 for yes or 0 for no")
    try:
        save = int(input(" > "))
    except ValueError:
        print("ERROR: PLEASE ENTER AN INTEGER")
        return get_scan_type()
    else:
        if save != 0 and save != 1:
            print("ERROR: PLEASE NETER A VALID OPTION")
            return get_scan_type()
        else:
            return save

def scan(option_num):
    if option_num == 0: # OS information
        print("OS SYSTEM INFORMATION")
        os.system('(cat /proc/version || uname -a ) 2>/dev/null; lsb_release -a 2>/dev/null')
    elif option_num == 1: # SUDO version
        print("SUDO VERSION")    
        os.system('sudo -V 2>/dev/null')
    elif option_num == 2: # Environment variables information
        print("ENVIRONMENT VARIABLES INFORMATION")
        os.system('(env || set) 2>/dev/null')
    elif option_num == 3: # Defensive measures information
        print("DEFENSIVE MEASURES INFORMATION")    
        os.system('echo AppArmor:')
        os.system('if [ `which aa-status 2>/dev/null` ]; then aa-status; elif [ `which apparmor_status 2>/dev/null` ]; then apparmor_status; elif ls -d /etc/apparmor* 2>/dev/null; then echo; else echo "Not found AppArmor"; fi')
    elif option_num == 4: # Dmesg signature authentication failed
        print("DMESG SIGNATURE INFORMATION")    
        os.system('dmesg 2>/dev/null | grep "signature"')

def scan_to_file(option_num, filename):
    if option_num == 0: # OS information
        os.system('(echo "########## OS SYSTEM INFORMATION ##########") >> %s' % (filename))
        os.system('((cat /proc/version || uname -a ) 2>/dev/null; lsb_release -a 2>/dev/null) >> %s' % (filename))
    elif option_num == 1: # SUDO version
        os.system('(echo "########## SUDO VERSION ##########") >> %s' % (filename))    
        os.system('(sudo -V 2>/dev/null) >> %s' % (filename))
    elif option_num == 2: # Environment variables information
        os.system('(echo "########## ENVIRONMENT VARIABLES INFORMATION ##########") >> %s' % (filename))
        os.system('((env || set) 2>/dev/null) >> %s' % (filename))
    elif option_num == 3: # Defensive measures information
        os.system('(echo "########## DEFENSIVE MEASURES INFORMATION ##########") >> %s' % (filename))
        os.system('(echo AppArmor:) >> %s' % (filename))
        os.system('(if [ `which aa-status 2>/dev/null` ]; then aa-status; elif [ `which apparmor_status 2>/dev/null` ]; then apparmor_status; elif ls -d /etc/apparmor* 2>/dev/null; then echo; else echo "Not found AppArmor"; fi) >> %s' % (filename))
    elif option_num == 4: # Dmesg signature authentication failed
        os.system('(echo "########## DMESG SIGNATURE INFORMATION ##########") >> %s' % (filename))
        os.system('(dmesg 2>/dev/null | grep "signature") >> %s' % (filename))
 
def main():
    scan_type = get_scan_type()
    scan_options = []
    if scan_type == 0: #if it is a custom scan
    	scan_options = get_custom_options()
    	
    # This asks the user if they want to save the results of their scan to a file, and if they do, it asks the user what name they want to give to the file
    save_choice = get_save()
    filename = "scan_file.txt"
    
    if scan_type == 0:
        print("Custom scan commencing...")
        if save_choice == 0:
            for i in scan_options:
    	        scan(i)
        else:
            for i in scan_options:
                scan_to_file(i, filename)
    else:
        print("Full scan commencing...")
        full_scan_options = [0,1,2,3,4]
        if save_choice == 0:
            for i in full_scan_options:
                scan(i)
        else:
            for i in full_scan_options:
                scan_to_file(i, filename)
    print("The scan has been completed")


if __name__=='__main__':
    main()
