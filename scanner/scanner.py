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
    Text = Yellow


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
            choice = int(input(f"({Colour.Text}{option}{Colour.Reset}) > "))
            if 0 <= choice <= range:
                return choice
        except Exception:
            display("Invalid Option")
    return choice

def display(text):
    print(f"\n{Colour.Colour1}[{Colour.Colour3}+{Colour.Colour1}]{Colour.Text} {text}{Colour.Reset}\n")

def requestweb(type, value, port, word):
    globaltype[0] = type
    r = requests.get(f"{type}://{value}:{port}/{word.strip()}")
    if r.status_code == 200:
        code200.append(word.strip())
    elif r.status_code == 403:
        code403.append(word.strip())

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
            tmp = "scan"
            while True:
                display("Options   [1] Dirb   [2] Save Scan   [3] Exit")
                option = getinput("options",4)
                if option == 1:
                    display("Which port would you like to dirb <exit - 4>")
                    for index, port in enumerate(ports):
                        print(f"{index} - {port}")
                    print("\n")
                    choice = getinput("dirb", len(ports))
                    if choice == 4:
                        display("Exited")
                    else:
                        with open("wordlists/common.txt") as wordlist:
                            words = wordlist.readlines()
                        global code200, code403, globaltype
                        code200, code403 = [],[]
                        globaltype = ["none"]
                        try:
                            if requests.get(f"https://{value}:{ports[choice]}/").status_code == 200:
                                [requestweb("https", value, ports[choice], word) for word in words]
                        except:
                            try:
                                if requests.get(f"http://{value}:{ports[choice]}/").status_code == 200:
                                    [requestweb("http", value, ports[choice], word) for word in words]
                            except:
                                print("Port not scannable")
                        file = open(".dirb", "w")
                        print(f"Code {Colour.Green}200{Colour.Reset}")
                        file.write(f"Code {Colour.Green}200{Colour.Reset}")
                        for word in code200:
                            print(f"{globaltype[0]}://{value}:{ports[choice]}/{word}")
                            file.write(f"{globaltype[0]}://{value}:{ports[choice]}/{word}")
                        print(f"\n{Colour.Red}Code 403{Colour.Reset}\n")
                        file.write(f"\n{Colour.Red}Code 403{Colour.Reset}\n")
                        for word in code403:
                            print(f"{globaltype[0]}://{value}:{ports[choice]}/{word}")
                            file.write(f"{globaltype[0]}://{value}:{ports[choice]}/{word}")
                        file.close()
                        tmp = "dirb"
                elif option == 2:
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
                    display("Exited")
                    break
            else:
                display(f"\nInvalid Parameters:{help}")


if __name__ == "__main__":
    print(f"""{Colour.Blue}
   _____
  / ____|
 | (___    ___  __ _  _ __   _ __    ___  _ __
  \___ \  / __|/ _` || '_ \ | '_ \  / _ \| '__|
  ____) || (__| (_| || | | || | | ||  __/| |
 |_____/  \___|\__,_||_| |_||_| |_| \___||_|\n{Colour.Red}\n{94*'-'}{Colour.Reset}""")
    main(sys.argv[1:])
    os.system("rm .scan 2>/dev/null")
