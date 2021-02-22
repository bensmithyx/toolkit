#!/usr/bin/env python3
import os, subprocess, sys, re, getopt, signal, socket
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
    Colour1 = Green
    Colour2 = Cyan
    Colour3 = Red
    Colour4 = White

def scanner(ip):
    ports, services = [], []
    try:
        for port in range(1,10000):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            if result == 0:
                ports.append(port)
                print(f"Port {port}: 	 Open")
            sock.close()
        return ports, services

    except KeyboardInterrupt:
        print("Exiting")
        sys.exit()

    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    except socket.error:
        print("Couldn't connect to server")
        sys.exit()
# When ctrl+c is pressed listfile with be removed to clean up the directory
def crash(sig, frame):
    os.system("rm .nmap .awkedfile 2>/dev/null")
    display("Exited")
    sys.exit(0)

# Catches ctrl+z signal
signal.signal(signal.SIGINT, crash)

def readfile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    file.close()
    return lines

def getinput(option,range):
    while True:
        try:
            choice = int(input(f"({Colour.Yellow}{option}{Colour.Reset}) > "))
            if 0 < choice <= range:
                return choice
        except Exception:
            display("Invalid Option")
    return choice

def display(text):
    print(f"\n{Colour.Blue}[{Colour.Red}+{Colour.Blue}]{Colour.Yellow} {text}{Colour.Reset}\n")

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
{Colour.Colour2}--targethost{Colour.Reset}      {Colour.Magenta}-t{Colour.Reset}
  {Colour.Colour3}n/a{Colour.Reset}
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
            #pattern = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
            #valid_ip = pattern.match(value)
            ip = socket.gethostbyname(value)
            display(f"Scanning {value}")
            ports, services = scanner(value)
            while True:
                display("Options   [1] Dirb   [2] Save nmap   [3] Exit")
                option = getinput("options",3)
                if option == 1:
                    display("Which port would you like to dirb")
                    for index, port in enumerate(ports):
                        print(f"{index+1} - {port}")
                    print("\n")
                    choice = getinput("dirb", len(ports))
                    os.system(f"dirb http://{value}:{ports[choice]}")
                elif option == 2:
                    file = open("nmap","w")
                    for line in readfile(".nmap"):
                        file.write(line)
                    file.close()
                    display("File save to nmap")
                elif option == 3:
                    display("Exited")
                    break
            else:
                print(f"\nInvalid Parameters:{help}")


if __name__ == "__main__":
   main(sys.argv[1:])
