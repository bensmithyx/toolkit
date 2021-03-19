#get the code from reverescripts.txt and output to screen splitting victim and attacker
def main():
    machine = int(input("Is this the Attacker machine (1) or the Victim machine (2)?\n"))
    if machine != 1 and machine != 2:
        print("Invalid input, try again")
        main()
    ip = input("Enter your ip address (ipv4):\n")
    port = input("Enter your port number:\n")

    file1 = open('reversescripts.txt','r+')
    lines = file1.readlines()
    machinetracker = False
    for line in lines:
        if line.strip() == "attacker" or line.strip() == "victim":
            print("\n")
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
            print(line.strip())
        
    file1.close()


if __name__=='__main__':
    main()