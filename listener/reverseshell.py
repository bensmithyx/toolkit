#!/usr/bin/env python3

import socket
import sys

def FormatCommands(ip,port,machine):
    file1 = open('reversescripts.txt','r+')
    lines = file1.readlines()
    machinetracker = False
    for line in lines:
        if line.strip() == "attacker" or line.strip() == "victim":
            if line.strip() == "attacker":
                machinetracker = False
            elif line.strip() == "victim":
                machinetracker = True # if victim was before then this is victim code so output victim code

        else:
            for i in line.strip():
                if i == '@':
                    line = line.replace("@",ip)
                elif i == '£':
                    line = line.replace("£",str(port))
            if machinetracker == True and machine == 1:
                print(line.strip())
            elif machinetracker == False and machine == 2:
                print(line.strip())
    file1.close()



def main():

    ################################# Initialising machines and taking ip/port #################################

    machine = int(input("Is this the Attacker machine (1) or the Victim machine (2)?\n"))
    if machine != 1 and machine != 2:
        print("Invalid input, try again")
        main()
    ip = input("Enter your ip address (ipv4):\n")
    port = input("Enter your port number:\n")



    ################################# Socket connection between machines #################################

    if machine == 1:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((socket.gethostname(),9002))
        sock.listen(1)
        connection = False
        while not connection:
            clientsocket, address = sock.accept()
            print(f"connection from {address} has been established")
            clientsocket.send(bytes("Welcome to the server","utf-8"))
#Testing here to see if machine 2 can load before machine 1 and vice versa for a connection
    elif machine == 2:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            sock.connect((socket.gethostname(),9002))
        except socket.error:                                                                   # try except added to provide error message instead of crashing
            print("Error :( Please load the script on the attacker machine first as this acts as the server :)")
            sys.exit(1)
        message = sock.recv(1024) # how big of chunks do we want to receive our tcp data
        print(message.decode("utf-8"))

    ################################# Inputting ip and port into reverseshell code #################################

    FormatCommands(ip,port,machine)

if __name__=='__main__':
    main()
