#!/bin/env python3
import os, subprocess, sys, re, getopt, signal, socket, requests, time
from datetime import datetime

# Adding in colourful text
class Colour:
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
    bracketsymbol = Blue
    normaltext = Cyan
    plussymbol = Red
    lines = White
    text = Yellow

# Each host scan is turned into an object so the data can be retrieved more easily
class Scan:
    def __init__(self,ports,statuses,services,host,time):
        self.ports = ports
        self.statuses = statuses
        self.services = services
        self.host = host
        self.time = time

# Each dirb scan will turn into an object so the data can be retrieved more easily
class Dirb:
    def __init__(self,files,host):
        self.files = files
        self.host = host

# When ctrl+c is pressed listfile with be removed to clean up the directory
def crash(sig, frame):
    display("Exited")
    sys.exit(0)

# Catches ctrl+c signal
signal.signal(signal.SIGINT, crash)

# Finds service of ports
def servicescan(port,protocal):
    try:
        service = socket.getservbyport(port, protocal)
        return service
    except:
        return False

# Scans host for open ports
def scanner(ip,portranges):
    top_ports = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8000]
    if portranges == "top-ports":
        portrange = top_ports
    elif portranges == "all-ports":
        portrange = list(range(65535))
    else:
        display("Invalid range set")
        return 0
    # Creating arrays for values of the ports, status of the ports and servivce of the ports to be populated with
    ports, statuses, services = [],[],[]
    try:
        display(f"Scanning ({Colour.Red}{ip}{Colour.Yellow})")
        # Scanning all ports 65535
        t1 = datetime.now()
        for port in portrange:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            if result == 0:
                ports.append(port)
                statuses.append("open")
                # If service is not found using tcp or udp it will be unknown
                service = servicescan(port,"tcp")
                if not service:
                    # If the service is not found for tcp or udp is will set service as unknown
                    if not servicescan(port,"udp"):
                        services.append("Unknown")
                else:
                    services.append(service)
            sock.close()
        t2 = datetime.now()
        scans.append(Scan(ports,statuses,services,ip,t2-t1))
    # If ctrl+c is pressed it will display "Exited"
    except KeyboardInterrupt:
        print("Exiting")
        sys.exit()
    except socket.gaierror:
        print('Hostname could not be resolved.')
        sys.exit()
    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

# Function to read files
def readfile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    file.close()
    return lines

# Function to get input with formated and coloured chacters
def getinput(option,range):
    while True:
        try:
            choice = int(input(f"({Colour.text}{option}{Colour.Reset}) > "))
            if 0 < choice <= range:
                return choice
            else:
                display("Invalid Option")
        except Exception:
            display("Invalid Option")
    return choice

# Displays text in a nice colourful format
def display(text):
    print(f"\n{Colour.bracketsymbol}[{Colour.plussymbol}+{Colour.bracketsymbol}]{Colour.text} {text}{Colour.Reset}\n")

# Checks if requests gets 200 or 403 response and appends the successfull attempts to an array
def requestweb(type, value, port, words, start):
    files = []
    recursivecheck = False
    globaltype[0] = type
    spaces = 0
    for word in words:
        word = word.strip()
        if start != "None":
            word = f"{start}/{word}"
        formattedword = word+(" "*spaces)
        spaces = len(word)
        print(f"{type}://{value}:{port}/{formattedword}", end="\r")
        r = requests.get(f"{type}://{value}:{port}/{word}")
        if r.status_code in [200,403]:
            # Checking if it is a file or directory
            try:
                recursive = requests.get(f"{type}://{value}:{port}/{word}/")
                if recursive.status_code in [200,403]:
                    recursivecheck = True
            except:
                pass
            if r.status_code == 200:
                # Formating output for cli and save file for 200 codes
                files.append("{}://{}:{}/{}{}{}{}{}200{}".format(type,value,port,'\x1b[1;34m' if recursivecheck == True else '\u001b[0m',word,Colour.Reset,(" "*(25-len(word))),Colour.Green,Colour.Reset))
                print("{}://{}:{}/{}{}{}{}{}200{}".format(type,value,port,'\x1b[1;34m' if recursivecheck == True else '\u001b[0m',word,Colour.Reset,(" "*(25-len(word))),Colour.Green,Colour.Reset))
            elif r.status_code == 403:
                # Formating output for cli and save file for 403 codes
                files.append("{}://{}:{}/{}{}{}{}{}403{}".format(type,value,port,'\x1b[1;34m' if recursivecheck == True else '\u001b[0m',word,Colour.Reset,(" "*(25-len(word))),Colour.Red,Colour.Reset))
                print("{}://{}:{}/{}{}{}{}{}403{}".format(type,value,port,'\x1b[1;34m' if recursivecheck == True else '\u001b[0m',word,Colour.Reset,(" "*(25-len(word))),Colour.Red,Colour.Reset))
            if recursivecheck:
                requestweb(type, value, port, words, word)
    # Clearing last output
    print(" "*50, end="\r")
    dirbslist.append(Dirb(files,value))

# Start of the main body of code
def main(argv):
    global scans, dirbslist
    scans = []
    dirbslist = []
    verbose = False
    # Options for argument inputation
    short_options = "ht:"
    long_options = ["help", "target="]
    # Help menu for users
    help = f"""\n{Colour.lines}

  _    _ ______ _      _____
 | |  | |  ____| |    |  __ \\
 | |__| | |__  | |    | |__) |
 |  __  |  __| | |    |  ___/
 | |  | | |____| |____| |
 |_|  |_|______|______|_|
---------------------------------------------------------------------------------------------{Colour.Reset}
{Colour.normaltext}long argument{Colour.Reset}   {Colour.Magenta}short argument{Colour.Reset}    {Colour.plussymbol}value{Colour.Reset}
{Colour.lines}---------------------------------------------------------------------------------------------{Colour.Reset}
{Colour.normaltext}--help{Colour.Reset}           {Colour.Magenta}-h{Colour.Reset}               {Colour.plussymbol}n/a{Colour.Reset}
{Colour.normaltext}--target{Colour.Reset}         {Colour.Magenta}-t{Colour.Reset}               {Colour.plussymbol}hostname{Colour.Reset}
{Colour.lines}---------------------------------------------------------------------------------------------{Colour.Reset}\n"""
    if len(argv) <1:
        display(f"An argument must be set{help}")
    try:
        arguments, values = getopt.getopt(argv, short_options, long_options)
    except getopt.error as error:
        # Output error, and return with an error code
        print(error)
        sys.exit(2)
    # Evaluate given options
    for current_argument, value in arguments:
        if current_argument in ("-h", "--help"):
            print(help)
        elif current_argument in ("-t", "--target"):
            try:
                # Checking if host is valid
                ip = socket.gethostbyname(value)
            except:
                display("Invalid host")
                sys.exit(0)
            # Displaying output of host scan to the user.
            # Running host scan
            scanner(value,"top-ports")
            print(f"PORT    STATUS    SERVICE\n")
            # Displaying output to cli and sotring output into a temp file in case it wants to be saved
            for port, status, service in zip(scans[-1].ports,scans[-1].statuses,scans[-1].services):
                print(f"{Colour.normaltext}{port}{' '*(8-len(str(port)))}{status}{' '*(10-len(str(status)))}{service}{Colour.Reset}\n{30*'-'}")
            print(f"\nScantime - {scans[-1].time}")
            # Setting default wordlist
            wordlist = "common.txt"
            portrange = "top-ports"
            while True:
                # Displaying options
                display("Options   [1] Scan   [2] Dirb   [3] Save   [4] Settings   [5] Exit")
                option = getinput("options",5)
                if option == 1:
                    try:
                        # Checking if host is valid
                        ip = socket.gethostbyname(input(f"({Colour.text}host{Colour.Reset}) > "))
                    except:
                        display("Invalid host")
                    else:
                        #
                        # Displaying output of host scan to the user.
                        # Scanning all ports
                        # Running host scan
                        scanner(value,portrange)
                        print(f"PORT    STATUS    SERVICE\n")
                        # Displaying output to cli and sotring output into a temp file in case it wants to be saved
                        for port, status, service in zip(scans[-1].ports,scans[-1].statuses,scans[-1].services):
                            print(f"{Colour.normaltext}{port}{' '*(8-len(str(port)))}{status}{' '*(10-len(str(status)))}{service}{Colour.Reset}\n{30*'-'}")
                        print(f"\nScantime - {scans[-1].time}")
                elif option == 2:
                    display(f"Which port would you like to dirb")
                    # Displaying all ports found
                    for index, port in enumerate(scans[-1].ports):
                        print(f"{index+1} - {port}")
                    print(f"{len(scans[-1].ports)+1} - Exit")
                    print("\n")
                    # Asking which port the user wants to input by showing them the ports found
                    choice = getinput("dirb", len(scans[-1].ports)+1)
                    if choice == len(scans[-1].ports)+1:
                        display("Exited")
                    else:
                        choice -=1
                        # Reading words from chosen wordlist
                        words = readfile(f"wordlists/{wordlist}")
                        global globaltype
                        globaltype = ["none"]
                        # Checking if host:port is valid and will then enumerate
                        try:
                            if requests.get(f"https://{value}:{scans[-1].ports[choice]}/").status_code == 200:
                                requestweb("https", value, scans[-1].ports[choice], words, "None")
                        except:
                            try:
                                if requests.get(f"http://{value}:{scans[-1].ports[choice]}/").status_code == 200:
                                    requestweb("http", value, scans[-1].ports[choice], words, "None")
                            except Exception as exception:
                                print(exception)
                                print("Port not scannable")
                elif option == 3:
                    # Allows the user to save both host scans and directory scans
                    display("Options   [1] Save Scan   [2] Save Dirb   [3] Exit")
                    option = getinput("options",3)

                    if option == 1:
                        display("Which scan would you like to save?")
                        for index, scan in enumerate(scans,1):
                            print(f"{index} - {scan.host}")
                        print(f"{len(scans)+1} - Exit\n")
                        choice = getinput("scans",len(scans)+1)
                        if choice == len(scans)+1:
                            display("Exited")
                        else:
                            file = open(f"{scans[choice-1].host}.scan","w")
                            file.write(f"PORT    STATUS    SERVICE\n")
                            for port, status, service in zip(scans[choice-1].ports,scans[choice-1].statuses,scans[choice-1].services):
                                file.write(f"\n{Colour.normaltext}{port}{' '*(8-len(str(port)))}{status}{' '*(10-len(str(status)))}{service}{Colour.Reset}\n{30*'-'}")
                            file.write(f"\nScantime - {scans[choice-1].time}")
                            file.close()
                            display(f"File save to {scans[choice-1].host}.scan")
                    if option == 2:
                        display("Which scan would you like to save?")
                        for index, dirbscan in enumerate(dirbslist,1):
                            print(f"{index} - {dirbscan.host}")
                        print(f"{len(dirbslist)+1} - Exit\n")
                        choice = getinput("scans",len(dirbslist)+1)
                        if choice == len(dirbslist)+1:
                            display("Exited")
                        else:
                            file = open(f"{dirbslist[choice-1].host}.dirb","w")
                            for directory in dirbslist[choice-1].files:
                                file.write(f"{directory}\n")
                            file.close()
                            display(f"File save to {dirbslist[choice-1].host}.dirb")
                    elif option == 3:
                        display("Exited")
                elif option == 4:
                    while True:
                        display(f"Settings    [1] Wordlist({Colour.Red}{wordlist}{Colour.Yellow})    [2] Port Range({Colour.Red}{portrange}{Colour.Yellow})    [3] Exit{Colour.Reset}")
                        choice = getinput("Settings", 3)
                        if choice == 1:
                            # Fidning all txt files in wordlist so directories are ignored
                            directory = os.listdir("wordlists")
                            for index, list in enumerate(directory, 1):
                                if list[-4:] == ".txt":
                                    print(f"{index} - {list}")
                            print(f"{len(directory)+1} - Exit\n")
                            choice = getinput("wordlists", len(directory)+1)-1
                            if choice == len(directory):
                                display("Exited")
                            else:
                                wordlist = directory[choice]
                                display(f"Set wordlist to {Colour.Red}{wordlist}{Colour.Reset}")
                        elif choice == 2:
                            portranges = ["top-ports","all-ports","Exit"]
                            for index, label in enumerate(portranges,1):
                                print(f"{index} - {label}")
                            choice = getinput("portsrange", 3)-1
                            if portranges[choice] == "Exit":
                                display("Exited")
                            else:
                                portrange = portranges[choice]
                                display(f"Set port range to {Colour.Red}{portrange}{Colour.Reset}")
                        elif choice == 3:
                            display("Exited")
                            break
                elif option == 5:
                    display("Exited")
                    break
            else:
                display(f"\nInvalid Parameters:{help}")

if __name__ == "__main__":
    # Title for program starts
    print(f"""{Colour.Blue}
   _____
  / ____|
 | (___    ___  __ _  _ __   _ __    ___  _ __
  \___ \  / __|/ _` || '_ \ | '_ \  / _ \| '__|
  ____) || (__| (_| || | | || | | ||  __/| |
 |_____/  \___|\__,_||_| |_||_| |_| \___||_|\n{Colour.Red}\n{94*'-'}{Colour.Reset}""")
    file = open(".dirb","w").close()
    main(sys.argv[1:])
    # Deletes tm files when prgram is exited
