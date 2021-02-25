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
    Colour1 = Blue
    Colour2 = Cyan
    Colour3 = Red
    Colour4 = White
    Text = Yellow


# When ctrl+c is pressed listfile with be removed to clean up the directory
def crash(sig, frame):
    os.system("rm .scan .dirb 2>/dev/null")
    display("Exited")
    sys.exit(0)

# Catches ctrl+c signal
signal.signal(signal.SIGINT, crash)

# Finds service of ports
def servicescan(port,protocal):
    try:
        print(f"{Colour.Colour2}{port}{' '*(8-len(str(port)))}{socket.getservbyport(port, protocal)}{Colour.Reset}\n{30*'-'}")
        file = open(".scan","a")
        file.write(f"\n{Colour.Colour2}{port}{' '*(8-len(str(port)))}{socket.getservbyport(port, protocal)}{Colour.Reset}\n{30*'-'}")
        file.close()
        return True
    except:
        return False

# Scans host for open ports
def scanner(ip):
    ports = []
    try:
        # Opening file to append scan
        file = open(".scan","w")
        print(f"PORT    SERVICE\n")
        file.write(f"PORT    SERVICE\n{30*'-'}")
        file.close()
        # Scanning all ports
        for port in range(65535):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            if result == 0:
                ports.append(port)
                # if service is not found using tcp or udp it will be unknown
                if not servicescan(port,"tcp"):
                    if not servicescan(port,"udp"):
                        file = open(".scan","a")
                        print(f"{Colour.Colour2}{port}{' '*(8-len(str(port)))}Unknown{Colour.Reset}\n{30*'-'}")
                        file.write(f"\n{Colour.Colour2}{port}{' '*(8-len(str(port)))}Unknown{Colour.Reset}\n{30*'-'}")
                        file.close()
            sock.close()
        return ports
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
            choice = int(input(f"({Colour.Text}{option}{Colour.Reset}) > "))
            if 0 <= choice <= range:
                return choice
        except Exception:
            display("Invalid Option")
    return choice
# Displays text in a nice colourful format
def display(text):
    print(f"\n{Colour.Colour1}[{Colour.Colour3}+{Colour.Colour1}]{Colour.Text} {text}{Colour.Reset}\n")
# Checks if requests gets 200 or 403 response and appends the successfull attempts to an array
def requestweb(type, value, port, words, start):
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
            try:
                recursive = requests.get(f"{type}://{value}:{port}/{word}/")
                if recursive.status_code in [200,403]:
                    recursivecheck = True
            except:
                print("here")
            file = open(".dirb","a")
            if r.status_code == 200:
                print("{}://{}:{}/{}{}{}{}{}200{}".format(type,value,port,'\x1b[1;34m' if recursivecheck == True else '\u001b[0m',word,Colour.Reset,(" "*(25-len(word))),Colour.Green,Colour.Reset))
                file.write("\n{}://{}:{}/{}{}{}{}{}200{}".format(type,value,port,'\x1b[1;34m' if recursivecheck == True else '\u001b[0m',word,Colour.Reset,(" "*(25-len(word))),Colour.Green,Colour.Reset))
            elif r.status_code == 403:
                print("{}://{}:{}/{}{}{}{}{}403{}".format(type,value,port,'\x1b[1;34m' if recursivecheck == True else '\u001b[0m',word,Colour.Reset,(" "*(25-len(word))),Colour.Red,Colour.Reset))
                file.write("\n{}://{}:{}/{}{}{}{}{}403{}".format(type,value,port,'\x1b[1;34m' if recursivecheck == True else '\u001b[0m',word,Colour.Reset,(" "*(25-len(word))),Colour.Red,Colour.Reset))
            file.close()
            if recursivecheck:
                requestweb(type, value, port, words, word)
# Start of the main body of code
def main(argv):
    verbose = False
    # Options for argument inputation
    short_options = "ht:"
    long_options = ["help", "targethost="]
    # Help menu for users
    help = f"""\n{Colour.Colour4}

  _    _ ______ _      _____
 | |  | |  ____| |    |  __ \\
 | |__| | |__  | |    | |__) |
 |  __  |  __| | |    |  ___/
 | |  | | |____| |____| |
 |_|  |_|______|______|_|
---------------------------------------------------------------------------------------------{Colour.Reset}
{Colour.Colour2}long argument{Colour.Reset}   {Colour.Magenta}short argument{Colour.Reset}    {Colour.Colour3}value{Colour.Reset}
{Colour.Colour4}---------------------------------------------------------------------------------------------{Colour.Reset}
{Colour.Colour2}--help{Colour.Reset}           {Colour.Magenta}-h{Colour.Reset}               {Colour.Colour3}n/a{Colour.Reset}
{Colour.Colour2}--targethost{Colour.Reset}     {Colour.Magenta}-t{Colour.Reset}               {Colour.Colour3}n/a{Colour.Reset}
{Colour.Colour4}---------------------------------------------------------------------------------------------{Colour.Reset}\n"""
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
            print(f"\nDisplaying help:{help}")
        elif current_argument in ("-t", "--targethost"):
            try:
                # Checking if host is valid
                ip = socket.gethostbyname(value)
            except:
                display("Invalid host")
                sys.exit(0)
            # Starting host scan
            display(f"Scanning {value}")
            t1 = datetime.now()
            ports = scanner(value)
            t2 = datetime.now()
            print(f"\nScantime - {t2-t1}")
            file = open(".scan","a")
            file.write(f"\nScantime - {t2-t1}")
            file.close()
            tmp = "scan"
            wordlist = "common.txt"
            while True:
                # Displaying options
                display("Options   [1] Dirb   [2] Save Scan   [3] Settings   [4] Exit")
                option = getinput("options",4)
                if option == 1:
                    display(f"Which port would you like to dirb <exit - {len(ports)+1}>")
                    for index, port in enumerate(ports):
                        print(f"{index} - {port}")
                    print("\n")
                    # Asking which port the user wants to input by showing them the ports found
                    choice = getinput("dirb", len(ports)+1)
                    if choice == len(ports)+1:
                        display("Exited")
                    else:
                        # Reading words from chosen wordlist
                        words = readfile(f"wordlists/{wordlist}")
                        global globaltype
                        globaltype = ["none"]
                        # Checking if host:port is valid and will then enumerate
                        try:
                            if requests.get(f"https://{value}:{ports[choice]}/").status_code == 200:
                                requestweb("https", value, ports[choice], words, "None")
                        except:
                            try:
                                if requests.get(f"http://{value}:{ports[choice]}/").status_code == 200:
                                    requestweb("http", value, ports[choice], words, "None")
                            except:
                                print("Port not scannable")
                        tmp = "dirb"
                elif option == 2:
                    # If save it chosen it will save the desired output to a file
                    tmpfile = ".scan"
                    filename = "scan"
                    if tmp == "dirb":
                        tmpfile = ".dirb"
                        filename = "dirb"
                    file = open(filename,"w")
                    for line in readfile(tmpfile):
                        file.write(line)
                    file.close()
                    display(f"File save to {filename}")
                elif option == 3:
                    display(f"Settings    [1] Wordlist({Colour.Red}{wordlist}{Colour.Yellow})   [2] Exit{Colour.Reset}")
                    choice = getinput("Settings", 2)
                    if choice == 1:
                        # Fidning all txt files in wordlist so directories are ignored
                        directory = os.listdir("wordlists")
                        for index, list in enumerate(directory):
                            if list[-4:] == ".txt":
                                print(f"{index} - {list}")
                        choice = getinput("wordlists", len(directory))
                        wordlist = directory[choice]
                        display(f"Set wordlist to {Colour.Red}{wordlist}{Colour.Reset}")
                    elif choice == 2:
                        display("Exited")
                elif option == 4:
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
    os.system("rm .scan .dirb 2>/dev/null")
