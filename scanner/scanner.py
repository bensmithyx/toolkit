#!/usr/bin/env python3
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
    text = Yellow


# When ctrl+c is pressed listfile with be removed to clean up the directory
def crash(sig, frame):
    os.system("rm .scan 2>/dev/null")
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
        file = open(".scan","w")
        print(f"PORT    SERVICE\n")
        file.write(f"PORT    SERVICE\n{30*'-'}")
        file.close()
        for port in range(65535):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            if result == 0:
                ports.append(port)
                if not servicescan(port,"tcp"):
                    if not servicescan(port,"udp"):
                        file = open(".scan","a")
                        print(f"{Colour.Colour2}{port}{' '*(8-len(str(port)))}Unknown{Colour.Reset}\n{30*'-'}")
                        file.write(f"\n{Colour.Colour2}{port}{' '*(8-len(str(port)))}Unknown{Colour.Reset}\n{30*'-'}")
                        file.close()
            sock.close()
        file.close()
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

def readfile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    file.close()
    return lines

def getinput(option,range):
    while True:
        try:
            choice = int(input(f"({Colour.text}{option}{Colour.Reset}) > "))
            if 0 <= choice <= range:
                return choice
        except Exception:
            display("Invalid Option")
    return choice

def display(text):
    print(f"\n{Colour.Colour1}[{Colour.Colour3}+{Colour.Colour1}]{Colour.text} {text}{Colour.Reset}\n")

def requestweb(type, value, port, word):
    if requests.get(f"{type}://{value}:{port}/{word.strip()}").status_code == 200:
        print(f"{type}://{value}:{port}/{word.strip()} {Colour.Green}200{Colour.Reset}")


def main(argv):
    verbose = False
    short_options = "ht:"
    long_options = ["help", "targethost="]
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
        print(f"An argument must be set{help}")
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
                ip = socket.gethostbyname(value)
            except:
                display("Invalid host")
                sys.exit(0)
            display(f"Scanning {value}")
            t1 = datetime.now()
            ports = scanner(value)
            t2 = datetime.now()
            print(f"\nScantime - {t2-t1}")
            file = open(".scan","a")
            file.write(f"\nScantime - {t2-t1}")
            file.close()
            while True:
                display("Options   [1] Dirb   [2] Save Scan   [3] Exit")
                option = getinput("options",3)
                if option == 1:
                    display("Which port would you like to dirb")
                    for index, port in enumerate(ports):
                        print(f"{index} - {port}")
                    print("\n")
                    choice = getinput("dirb", len(ports))
                    with open("../wordlists/common.txt") as wordlist:
                        words = wordlist.readlines()
                    if requests.get(f"http://{value}:{ports[choice]}/").status_code == 200:
                        [requestweb("http", value, ports[choice], word) for word in words]
                    elif requests.get(f"https://{value}:{ports[choice]}/").status_code == 200:
                        [requestweb("https", value, ports[choice], word) for word in words]
                    else:
                        print("Port not scannable")
                    #os.system(f"dirb http://{value}:{ports[choice]}")
                elif option == 2:
                    file = open("scan","w")
                    for line in readfile(".scan"):
                        file.write(line)
                    file.close()
                    display("File save to scan")
                elif option == 3:
                    display("Exited")
                    break
            else:
                print(f"\nInvalid Parameters:{help}")


if __name__ == "__main__":
    main(sys.argv[1:])
    os.system("rm .scan 2>/dev/null")
