#get the code from reverescripts.txt and output to screen splitting victim and attacker
def main():
    ip = "172.23.90.233" #input("Enter your ip address")
    port = 4444 #input("Enter your port number")
    file1 = open('reversescripts.txt','r+')
    lines = file1.readlines()
    for line in lines:
        if line.strip() == "attacker" or line.strip() == "victim":
            print("\n",line.strip())
        else:
            #print(line.strip())
            for i in line.strip():
            #    print(i)
                if i == '@':
                    line = line.replace("@",ip)
                elif i == '£':
                    line = line.replace("£",str(port))
            print(line.strip())
        
    file1.close()


if __name__=='__main__':
    main()