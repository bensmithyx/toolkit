#!/usr/bin/env python3
from subprocess import check_output #used to get ips valid on machine
import re # for regex when getting ip
import os # for outputting command line commands
import socket # for sending the scan file to another machine

class Colour: #class of all the colours we may use
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

def get_scan_type():
    display("Which type of scan would you like to carry out?")
    scans = ["Custom scan","Light scan","Medium scan","Full scan"]
    for i in range(4):
        print(f"{Colour.Colour4}{i} - {Colour.Colour2}{scans[i]}{Colour.Reset}")
    try:
        scan = int(input(f"({Colour.Text}Scan Selection{Colour.Reset}) > "))
    except ValueError:
        displayerror("Error: please enter an integer value")
        return get_scan_type()
    else:
        if scan not in range(4):
            displayerror("Option entered not in correct range, try again")
            return get_scan_type()
        return scan

def get_custom_options():
    options = []
    
    enter_options_again = True
    while enter_options_again == True:
        # Asks the user which scan options they want in their custom scan, showing the user which scan options correlate to which scan number.
        display("Which scan options would you like to include?")
        print(f"{Colour.Colour2}Enter the option numbers with a space between each one, eg '2 7 16'{Colour.Reset}")
        option_list = ["OS information","SUDO version","Environment variable information","Defences information","DMESG signature information","Drive information","Root owned cron jobs","Root owned running processes","Timers","Sockets","D-BUS","Network information","Information on current user","Information on all users","SUDO permissions","Clipboard and highlighted text","PGP keys","Common password brute force","List of useful binaries","Screen and TMUX sessions","Root owned SUID/SGID files","File permissions of sensitive files","Hashes in passwd file","Path information","Hidden files","Log files","Writeable files","Recently modified files", "Files containing passwords","Files with unexpected ACL"]
        for i in range(len(option_list)):
            print(f"{Colour.Colour4}{i} - {Colour.Colour2}{option_list[i]}{Colour.Reset}")
    
        # gets the scan options that the user wants by searching the user input for each of the scan option numbers and placing them into their own list. This means that the option numbers are now stored in the correct order and duplicates are eliminated.
        user_input = " " + input(f"({Colour.Text}Option Selection{Colour.Reset}) > ") + " "
        for i in range(len(option_list)):
            if user_input.find(" " + str(i) + " ") != -1:
                options.append(i)
    
        # shows the user what the computer has interpreted as their scan from their input.
        print(f"\n{Colour.Colour2}Your scan: ", end=" ")
        for i in options:
            if i != options[len(options) - 1]:
                print(option_list[i], end=", ")
            else:
                print(f"{option_list[i]}{Colour.Reset}")
    
        # asks the user if they are happy with these options, or if they want to try chosing their options again
        reenter_options = ""
        while reenter_options != "1" and reenter_options != "0":
            display("Are you happy with the options you have selected?")
            answer_options = ["No","Yes"]
            for i in range(2):
                print(f"{Colour.Colour4}{i} - {Colour.Colour2}{answer_options[i]}{Colour.Reset}")

            reenter_options = input(f"({Colour.Text}Option Confirmation{Colour.Reset}) > ")
            if reenter_options == "1":
                return options
            elif reenter_options == "0":
                options = []
            else:
                displayerror("Invalid option, try again")
             
def get_save():
    display("Would you like to save the scan to a file?")
    options = ["No","Yes"]
    for i in range(2):
        print(f"{Colour.Colour4}{i} - {Colour.Colour2}{options[i]}{Colour.Reset}")
    try:
        save = int(input(f"({Colour.Text}Save Selection{Colour.Reset}) > "))
    except ValueError:
        displayerror("Error, please enter an integer value")
        return get_save()
    else:
        if save not in range(2):
            displayerror("Option entered not in correct range, try again")
            return get_save()
        return save

def get_filename():
    valid_filename = False
    while valid_filename == False:
        display("Enter the name you want to save the file as")
        name = input(f"({Colour.Text}Filename Selection{Colour.Reset}) > ") + ".txt"
        try:
            f = open(name,"x")
        except FileExistsError:
            displayerror("File already exists, please try a different filename")
        except:
            displayerror("Filename is not valid, please try a different filename")
        else:
            f.close()
            valid_filename = True
    return name

def get_export():
    display("Would you like to send the file to another machine?")
    options = ["No","Yes"]
    for i in range(2):
        print(f"{Colour.Colour4}{i} - {Colour.Colour2}{options[i]}{Colour.Reset}")
    try:
        save = int(input(f"({Colour.Text}Export Selection{Colour.Reset}) > "))
    except ValueError:
        displayerror("Error, please enter an integer value")
        return get_save()
    else:
        if save not in range(2):
            displayerror("Option entered not in correct range, try again")
            return get_save()
        return save

def export(scan_filename):
    # get the ip address of the destination machine
    ask_for_ip = True
    while ask_for_ip == True:
        display("Enter the IP address of the machine that you want to send the file to")
        ip_address = input(f"({Colour.Text}IP Address Selection{Colour.Reset}) > ")
        if re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ip_address) != None: # regex from https://stackoverflow.com/questions/106179/regular-expression-to-match-dns-hostname-or-ip-address/106223#106223 and https://stackoverflow.com/questions/10086572/ip-address-validation-in-python-using-regex
            ask_for_ip = False # if the IP is in the correct format, then break out of the loop
        else:
            displayerror("IP address invalid, please try again!")
    
    # get the port number of the destination machine
    ask_for_port = True
    while ask_for_port == True:
        display("Enter the port on the machine that you want to send the file to")
        try:
            port = int(input(f"({Colour.Text}Port Selection{Colour.Reset}) > "))
        except ValueError:
            displayerror("Error, please enter an integer value")
        else:
            if port >= 1 and port <= 65535:
                ask_for_port = False # if the port is in the correct range, then break out of the loop
            else:
                displayerror("Port invalid, please try again!")
    
    # send the file to the destination machine
    display("Press enter when you have set up a TCP listener on port " + str(port) + " on the destination machine")
    input(f"{Colour.Colour2}For example: nc -l <PORT_NUMBER> >> <FILENAME>{Colour.Reset}")
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port))
        try:
            f = open(scan_filename, 'rb')
            scan_text = f.read(1024)
            while(scan_text):
                client_socket.send(scan_text)
                scan_text = f.read()
            f.close()
        except OSError:
            displayerror("Error, scan file not found!")
        client_socket.close()
    except OSError:
        displayerror("Error, connection failed!")
        
def title(name):
    os.system('echo ')
    #print(output)
    os.system('%s %s %s' % ("echo '########## ", str(name), " ##########'"))
    os.system('echo ')

def scan(option_num):
    if option_num == 0: # OS information
        title("OS SYSTEM INFORMATION")
        os.system('(cat /proc/version || uname -a ) 2>/dev/null; lsb_release -a 2>/dev/null')
    elif option_num == 1: # SUDO version
        title("SUDO VERSION")    
        os.system('sudo -V 2>/dev/null')
    elif option_num == 2: # Environment variables information
        title("ENVIRONMENT VARIABLES INFORMATION")
        os.system('(env || set) 2>/dev/null')
    elif option_num == 3: # Defensive measures information
        title("DEFENSIVE MEASURES INFORMATION")    
        os.system('echo AppArmor:')
        os.system('if [ `which aa-status 2>/dev/null` ]; then aa-status; elif [ `which apparmor_status 2>/dev/null` ]; then apparmor_status; elif ls -d /etc/apparmor* 2>/dev/null; then echo; else echo "Not found AppArmor"; fi')
        os.system('echo && echo Grsecurity:')
        os.system('((uname -r | grep "\-grsec" >/dev/null 2>&1 || grep "grsecurity" /etc/sysctl.conf >/dev/null 2>&1) && echo "Yes" || echo "Not found grsecurity")')
        os.system('echo && echo PaX:')
        os.system('(which paxctl-ng paxctl >/dev/null 2>&1 && echo "Yes" || echo "Not found PaX")')
        os.system('echo && echo Execshield:')
        os.system('(grep "exec-shield" /etc/sysctl.conf || echo "Not found Execshield")')
        os.system('echo && echo SElinux:')
        os.system('(sestatus 2>/dev/null || echo "Not found sestatus")')
        os.system('echo && echo ASLR:')
        os.system('if [ `cat /proc/sys/kernel/randomize_va_space 2>/dev/null` ]; then if [ `cat /proc/sys/kernel/randomize_va_space 2>/dev/null | grep 1` ]; then echo "Conservative Randomization enabled"; elif [ `cat /proc/sys/kernel/randomize_va_space 2>/dev/null | grep 2` ]; then echo "Full Randomization enabled"; else echo "ASLR disabled"; fi; fi')
    elif option_num == 4: # Dmesg signature authentication failed
        title("DMESG SIGNATURE INFORMATION")    
        os.system('dmesg 2>/dev/null | grep "signature"')
    elif option_num == 5: # Drives
        title("DEVICE INFORMATION")    
        os.system('echo Date:')
        os.system('date 2>/dev/null')
        os.system('echo && echo System Stats:')
        os.system('(df -h || lsblk))')
        os.system('echo && echo CPU:')
        os.system('lscpu')
        os.system('echo && echo Printers:')
        os.system('lpstat -a 2>/dev/null')
    elif option_num == 6: # List of cron jobs
        title("CRON JOB INFORMATION")    
        os.system('crontab -l 2>/dev/null; ls -al /etc/cron* /etc/at* 2>/dev/null; cat /etc/cron* /etc/at* /etc/anacrontab /var/spool/cron/crontabs/root 2>/dev/null | grep -v "^#"')
    elif option_num == 7: # List of running processes
        title("PROCESSES INFORMATION")    
        os.system('ps aux 2>/dev/null')
    elif option_num == 8: # Check timers
        title("TIMERS")    
        os.system('systemctl list-timers --all | cat')
    elif option_num == 9: # Look at sockets
        title("SOCKETS")    
        os.system('netstat -a -p --unix') #outputs alot of info
    elif option_num == 10: # D-BUS
        title("D-BUS INFORMATION")    
        os.system('busctl list 2>/dev/null')
    elif option_num == 11: # Network information
        title("NETWORK INFORMATION")
        os.system('echo IP addresses:')
        os.system('(ip addr show || ifconfig) 2>/dev/null')
        os.system('echo && echo Ports:')
        os.system('(ss -auntp || netstat -auntp) 2>/dev/null')
        os.system('echo && echo Routing:')
        os.system('(ip route show || route -n) 2>/dev/null')
        os.system('echo && echo ARP cache:')
        os.system('(ip neigh show || arp -n) 2>/dev/null')
    elif option_num == 12: # Current user information
        title("CURRENT USER INFORMATION")    
        os.system('id || (whoami && groups) 2>/dev/null')
    elif option_num == 13: # All user information
        title("INFORMATION ON ALL USERS")    
        os.system('''cat /etc/passwd | cut -d: -f1; cat /etc/passwd | grep "sh$"; awk -F: '($3 == "0") {print}' /etc/passwd; w; last | tail; lastlog; for i in $(cut -d":" -f1 /etc/passwd 2>/dev/null);do id $i;done 2>/dev/null | sort''')
    elif option_num == 14: # SUDO permissions
        title("SUDO PERMISSIONS")    
        os.system('sudo -ln 2>/dev/null && sudo -l 2>/dev/null; cat /etc/sudoers 2>/dev/null')
    elif option_num == 15: # Clipboard and highlighted text
        title("CLIPBOARD AND HIGHLIGHTED TEXT")    
        os.system('if [ `which xclip 2>/dev/null` ]; then echo "Clipboard: "`xclip -o -selection clipboard 2>/dev/null`; echo "Highlighted text: "`xclip -o 2>/dev/null`; elif [ `which xsel 2>/dev/null` ]; then echo "Clipboard: "`xsel -ob 2>/dev/null`; echo "Highlighted text: "`xsel -o 2>/dev/null`; else echo "Not found xsel and xclip"; fi')
    elif option_num == 16: # PGP keys
        title("PGP KEYS")    
        os.system('gpg --list-keys 2>/dev/null')
    elif option_num == 17: # Common password list brute force
        title("COMMON PASSWORD BRUTE FORCE")
        try:
            password_file = open("password_list.txt", "r")
            for line in password_file:
                os.system('echo %s | timeout 0.25 sudo -kS echo "Password found: %s" 2>/dev/null' % (line.strip(), line.strip()))
            password_file.close()
        except OSError:
            displayerror("Error, brute force password list not found!")
    elif option_num == 18: # Useful binaries list
        title("USEFUL BINARIES")    
        os.system('which nmap aws nc ncat netcat nc.traditional wget curl ping gcc g++ make gdb base64 socat python python2 python3 python2.7 python2.6 python3.6 python3.7 perl php ruby xterm doas sudo fetch docker lxc ctr runc rkt kubectl 2>/dev/null')
    elif option_num == 19: # Screen and TMUX sessions
        title("SCREEN AND TMUX SESSIONS")    
        os.system('echo Screen:')
        os.system('if [ `which screen 2>/dev/null` ]; then (screen -ls); else echo "Screen not found"; fi')
        os.system('echo && echo Tmux:')
        os.system('if [ `which tmux 2>/dev/null` ]; then (tmux ls); else echo "Tmux not found"; fi')
    elif option_num == 20: # Files with SUID or SGID bits set
        title("FILES WITH SUID SET")    
        os.system('find / -perm -4000 2>/dev/null')
        title("FILES WITH SGID SET") 
        os.system('find / -perm -2000 2>/dev/null')
    elif option_num == 21: # File permissions of sensitive files
        title("FILE PERMISSIONS FOR SENSITIVE FILES")    
        os.system('ls -l /etc/passwd 2>/dev/null; ls -l /etc/shadow 2>/dev/null')
    elif option_num == 22: # Looking for hashes in /etc/passwd
        title("HASHES IN PASSWD FILE")    
        os.system('echo Passwd equivalent files:')
        os.system('cat /etc/passwd /etc/pwd.db /etc/master.passwd /etc/group 2>/dev/null')
        os.system('echo && echo Shadow equivalent files:')
        os.system('cat /etc/shadow /etc/shadow- /etc/shadow~ /etc/gshadow /etc/gshadow- /etc/master.passwd /etc/spwd.db /etc/security/opasswd 2>/dev/null')
        os.system('echo && echo Password hashes:')
        os.system("grep -v '^[^:]*:[x\*]' /etc/passwd /etc/pwd.db /etc/master.passwd /etc/group 2>/dev/null")
    elif option_num == 23: # Path information
        title("PATH INFORMATION")    
        os.system('echo $PATH 2>/dev/null')
    elif option_num == 24: # List of hidden files
        title("HIDDEN FILES")    
        os.system('find / -type f -iname ".*" -ls 2>/dev/null')
    elif option_num == 25: # Log files
        title("LOG FILES")    
        os.system('''if [ `which aureport 2>/dev/null` ]; then (aureport --tty 2>/dev/null | grep -E "su |sudo "; grep -RE 'comm="su"|comm="sudo"' /var/log* 2>/dev/null); else echo "To view log file information, please install 'aureport'"''')
    elif option_num == 26: # List of writeable files
        title("WRITEABLE FILES")
        # finds files owned by the user or that  are world writeable
        os.system("find / '(' -type f -or -type d ')' '(' '(' -user $USER ')' -or '(' -perm -o=w ')' ')' 2>/dev/null | grep -v '/proc/' | grep -v $HOME | sort | uniq")
        # finds files that are writeable by any group of the user
        os.system("for g in `groups`; do find \( -type f -or -type d \) -group $g -perm -g=w 2>/dev/null | grep -v '/proc/' | grep -v $HOME; done")
    elif option_num == 27: # List of recently modified files
        title("RECENTLY MODIFIED FILES")    
        os.system('find / -type f -mmin -5 ! -path "/proc/*" ! -path "/sys/*" ! -path "/run/*" ! -path "/dev/*" ! -path "/var/lib/*" 2>/dev/null')
    elif option_num == 28: # Searching files that contain passwords
        title("FILES CONTAINING PASSWORDS")    
        os.system('''intpwdfiles=`timeout 150 grep -RiIE "(pwd|passwd|password|PASSWD|PASSWORD|dbuser|dbpass).*[=:].+|define ?\('(\w*passw|\w*user|\w*datab)" $HOMESEARCH /var/www /usr/local/www/ $backup_folders_row /tmp /etc /root /mnt /Users /private 2>/dev/null`; printf "%s\n" "$intpwdfiles" | grep -I ".php:"| sort | uniq | head -n 70; printf "%s\n" "$intpwdfiles" | grep -vI ".php:" | grep -E "^/" | grep ":"| sort | uniq | head -n 70''')
    elif option_num == 29: # Unexpected ACL
        title("FILES WITH UNEXPECTED ACL")    
        os.system('getfacl -t -s -R -p /bin /etc /home /opt /root /sbin /usr /tmp 2>/dev/null')

def title_in_file(name, filename):
    os.system('echo ')
    #print(output)
    os.system('(%s %s %s) >> %s' % ("echo '########## ", str(name), " ##########'", filename))
    os.system('echo ')

def scan_to_file(option_num, filename):
    if option_num == 0: # OS information
        title_in_file("OS SYSTEM INFORMATION", filename)
        os.system('((cat /proc/version || uname -a ) 2>/dev/null; lsb_release -a 2>/dev/null) >> %s' % (filename))
    elif option_num == 1: # SUDO version
        title_in_file("SUDO VERSION", filename)    
        os.system('(sudo -V 2>/dev/null) >> %s' % (filename))
    elif option_num == 2: # Environment variables information
        title_in_file("ENVIRONMENT VARIABLES INFORMATION", filename) 
        os.system('((env || set) 2>/dev/null) >> %s' % (filename))
    elif option_num == 3: # Defensive measures information
        title_in_file("DEFENSIVE MEASURES INFORMATION", filename)     
        os.system('(echo AppArmor:) >> %s' % (filename))
        os.system('(if [ `which aa-status 2>/dev/null` ]; then aa-status; elif [ `which apparmor_status 2>/dev/null` ]; then apparmor_status; elif ls -d /etc/apparmor* 2>/dev/null; then echo; else echo "Not found AppArmor"; fi) >> %s' % (filename))
        os.system('(echo && echo Grsecurity:) >> %s' % (filename))
        os.system('(((uname -r | grep "\-grsec" >/dev/null 2>&1 || grep "grsecurity" /etc/sysctl.conf >/dev/null 2>&1) && echo "Yes" || echo "Not found grsecurity")) >> %s' % (filename))
        os.system('(echo && echo PaX:) >> %s' % (filename))
        os.system('((which paxctl-ng paxctl >/dev/null 2>&1 && echo "Yes" || echo "Not found PaX")) >> %s' % (filename))
        os.system('(echo && echo Execshield:) >> %s' % (filename))
        os.system('((grep "exec-shield" /etc/sysctl.conf || echo "Not found Execshield")) >> %s' % (filename))
        os.system('(echo && echo SElinux:) >> %s' % (filename))
        os.system('((sestatus 2>/dev/null || echo "Not found sestatus")) >> %s' % (filename))
        os.system('(echo && echo ASLR:) >> %s' % (filename))
        os.system('(if [ `cat /proc/sys/kernel/randomize_va_space 2>/dev/null` ]; then if [ `cat /proc/sys/kernel/randomize_va_space 2>/dev/null | grep 1` ]; then echo "Conservative Randomization enabled"; elif [ `cat /proc/sys/kernel/randomize_va_space 2>/dev/null | grep 2` ]; then echo "Full Randomization enabled"; else echo "ASLR disabled"; fi; fi) >> %s' % (filename))
    elif option_num == 4: # Dmesg signature authentication failed
        title_in_file("DMESG SIGNATURE INFORMATION", filename) 
        os.system('(dmesg 2>/dev/null | grep "signature") >> %s' % (filename))
    elif option_num == 5: # Drives
        title_in_file("DEVICE INFORMATION", filename) 
        os.system('(echo Date:) >> %s' % (filename))
        os.system('(date 2>/dev/null) >> %s' % (filename))
        os.system('(echo && echo System Stats:) >> %s' % (filename))
        os.system('(df -h || lsblk) >> %s' % (filename))
        os.system('(echo && echo CPU:) >> %s' % (filename))
        os.system('(lscpu) >> %s' % (filename))
        os.system('(echo && echo Printers:) >> %s' % (filename))
        os.system('(lpstat -a 2>/dev/null) >> %s' % (filename))
    elif option_num == 6: # Cron jobs belonging to the root user
        title_in_file("CRON JOB INFORMATION", filename) 
        os.system('(crontab -l 2>/dev/null; ls -al /etc/cron* /etc/at* 2>/dev/null; cat /etc/cron* /etc/at* /etc/anacrontab /var/spool/cron/crontabs/root 2>/dev/null | grep -v "^#") >> %s' % (filename))
    elif option_num == 7: # Running processes belonging to the root user
        title_in_file("PROCESSES INFORMATION", filename) 
        os.system('(ps aux 2>/dev/null) >> %s' % (filename))
    elif option_num == 8: # Check timers
        title_in_file("TIMERS", filename) 
        os.system('(systemctl list-timers --all | cat) >> %s' % (filename))
    elif option_num == 9: # Look at sockets
        title_in_file("SOCKETS", filename) 
        os.system('(netstat -a -p --unix) >> %s' % (filename)) #outputs alot of info
    elif option_num == 10: # D-BUS
        title_in_file("D-BUS", filename) 
        os.system('(busctl list 2>/dev/null) >> %s' % (filename))
    elif option_num == 11: # Network information
        title_in_file("NETWORK INFORMATION", filename) 
        os.system('(echo IP addresses:) >> %s' % (filename))
        os.system('((ip addr show || ifconfig) 2>/dev/null) >> %s' % (filename))
        os.system('(echo && echo Ports:) >> %s' % (filename))
        os.system('((ss -auntp || netstat -auntp) 2>/dev/null) >> %s' % (filename))
        os.system('(echo && echo Routing:) >> %s' % (filename))
        os.system('((ip route show || route -n) 2>/dev/null) >> %s' % (filename))
        os.system('(echo && echo ARP cache:) >> %s' % (filename))
        os.system('((ip neigh show || arp -n) 2>/dev/null) >> %s' % (filename))
    elif option_num == 12: # Current user information
        title_in_file("CURRENT USER INFORMATION", filename) 
        os.system('(id || (whoami && groups) 2>/dev/null) >> %s' % (filename))
    elif option_num == 13: # All user information
        title_in_file("INFORMATION ON ALL USERS", filename) 
        os.system('''(cat /etc/passwd | cut -d: -f1; cat /etc/passwd | grep "sh$"; awk -F: '($3 == "0") {print}' /etc/passwd; w; last | tail; lastlog; for i in $(cut -d":" -f1 /etc/passwd 2>/dev/null);do id $i;done 2>/dev/null | sort) >> %s''' % (filename))
    elif option_num == 14: # SUDO permissions
        title_in_file("SUDO PERMISSIONS", filename)
        os.system('(sudo -ln 2>/dev/null && sudo -l 2>/dev/null; cat /etc/sudoers 2>/dev/null) >> %s' % (filename))
    elif option_num == 15: # Clipboard and highlighted text
        title_in_file("CLIPBOARD AND HIGHLIGHTED TEXT", filename) 
        os.system('(if [ `which xclip 2>/dev/null` ]; then echo "Clipboard: "`xclip -o -selection clipboard 2>/dev/null`; echo "Highlighted text: "`xclip -o 2>/dev/null`; elif [ `which xsel 2>/dev/null` ]; then echo "Clipboard: "`xsel -ob 2>/dev/null`; echo "Highlighted text: "`xsel -o 2>/dev/null`; else echo "Not found xsel and xclip"; fi) >> %s' % (filename))
    elif option_num == 16: # PGP keys
        title_in_file("PGP KEYS", filename) 
        os.system('(gpg --list-keys 2>/dev/null) >> %s' % (filename))
    elif option_num == 17: # Common password list brute force
        title_in_file("COMMON PASSWORD BRUTE FORCE", filename) 
        try:
            password_file = open("password_list.txt", "r")
            for line in password_file:
                os.system('(echo %s | timeout 0.25 sudo -kS echo "Password found: %s" 2>/dev/null) >> %s' % (line.strip(), line.strip(), filename))
            password_file.close()
        except OSError:
            displayerror("Error, brute force password list not found!")
    elif option_num == 18: # Useful binaries list
        title_in_file("USEFUL BINARIES", filename) 
        os.system('(which nmap aws nc ncat netcat nc.traditional wget curl ping gcc g++ make gdb base64 socat python python2 python3 python2.7 python2.6 python3.6 python3.7 perl php ruby xterm doas sudo fetch docker lxc ctr runc rkt kubectl 2>/dev/null) >> %s' % (filename))
    elif option_num == 19: # Screen and TMUX sessions
        title_in_file("SCREEN AND TMUX SESSIONS", filename) 
        os.system('(echo Screen:) >> %s' % (filename))
        os.system('(if [ `which screen 2>/dev/null` ]; then (screen -ls); else echo "Screen not found"; fi) >> %s' % (filename))
        os.system('(echo && echo Tmux:) >> %s' % (filename))
        os.system('(if [ `which tmux 2>/dev/null` ]; then (tmux ls); else echo "Tmux not found"; fi) >> %s' % (filename))
    elif option_num == 20: # Root owned files with SUID or SGID bits set
        title_in_file("FILES WITH SUID AND SGID SET", filename) 
        os.system('(find / -perm -4000 2>/dev/null) >> %s' % (filename))
    elif option_num == 21: # File permissions of sensitive files
        title_in_file("FILE PERMISSIONS FOR SENSITIVE FILES", filename) 
        os.system('(ls -l /etc/passwd 2>/dev/null; ls -l /etc/shadow 2>/dev/null) >> %s' % (filename))
    elif option_num == 22: # Looking for hashes in /etc/passwd
        title_in_file("HASHES IN PASSWD FILE", filename) 
        os.system('(echo Passwd equivalent files:) >> %s' % (filename))
        os.system('(cat /etc/passwd /etc/pwd.db /etc/master.passwd /etc/group 2>/dev/null) >> %s' % (filename))
        os.system('(echo && echo Shadow equivalent files:) >> %s' % (filename))
        os.system('(cat /etc/shadow /etc/shadow- /etc/shadow~ /etc/gshadow /etc/gshadow- /etc/master.passwd /etc/spwd.db /etc/security/opasswd 2>/dev/null) >> %s' % (filename))
        os.system('(echo && echo Password hashes:) >> %s' % (filename))
        os.system("(grep -v '^[^:]*:[x\*]' /etc/passwd /etc/pwd.db /etc/master.passwd /etc/group 2>/dev/null) >> %s" % (filename))
    elif option_num == 23: # Path information
        title_in_file("PATH INFORMATION", filename) 
        os.system('(echo $PATH 2>/dev/null) >> %s' % (filename))
    elif option_num == 24: # List of hidden files
        title_in_file("HIDDEN FILES", filename) 
        os.system('(find / -type f -iname ".*" -ls 2>/dev/null) >> %s' % (filename))
    elif option_num == 25: # Log files
        title_in_file("LOG FILES", filename) 
        os.system('''(if [ `which aureport 2>/dev/null` ]; then (aureport --tty 2>/dev/null | grep -E "su |sudo "; grep -RE 'comm="su"|comm="sudo"' /var/log* 2>/dev/null); else echo "To view log file information, please install 'aureport'") >> %s''' % (filename))
    elif option_num == 26: # List of writeable files
        title_in_file("WRITEABLE FILES", filename)
        # finds files owned by the user or that  are world writeable
        os.system("(find / '(' -type f -or -type d ')' '(' '(' -user $USER ')' -or '(' -perm -o=w ')' ')' 2>/dev/null | grep -v '/proc/' | grep -v $HOME | sort | uniq) >> %s" % (filename))
        # finds files that are writeable by any group of the user
        os.system("(for g in `groups`; do find \( -type f -or -type d \) -group $g -perm -g=w 2>/dev/null | grep -v '/proc/' | grep -v $HOME; done) >> %s" % (filename))
    elif option_num == 27: # List of recently modified files
        title_in_file("RECENTLY MODIFIED FILES", filename) 
        os.system('(find / -type f -mmin -5 ! -path "/proc/*" ! -path "/sys/*" ! -path "/run/*" ! -path "/dev/*" ! -path "/var/lib/*" 2>/dev/null) >> %s' % (filename))
    elif option_num == 28: # Searching files that contain passwords
        title_in_file("FILES CONTAINING PASSWORDS", filename) 
        os.system('''(intpwdfiles=`timeout 150 grep -RiIE "(pwd|passwd|password|PASSWD|PASSWORD|dbuser|dbpass).*[=:].+|define ?\('(\w*passw|\w*user|\w*datab)" $HOMESEARCH /var/www /usr/local/www/ $backup_folders_row /tmp /etc /root /mnt /Users /private 2>/dev/null`; printf "%s\n" "$intpwdfiles" | grep -I ".php:"| sort | uniq | head -n 70; printf "%s\n" "$intpwdfiles" | grep -vI ".php:" | grep -E "^/" | grep ":"| sort | uniq | head -n 70) >> %s''' % (filename))
    elif option_num == 29: # ACL
        title_in_file("FILES WITH AN ACL", filename) 
        os.system('(getfacl -t -s -R -p /bin /etc /home /opt /root /sbin /usr /tmp 2>/dev/null) >> %s' % (filename))

def main():
    scan_type = get_scan_type()
    scan_options = []
    if scan_type == 0: #if it is a custom scan
    	scan_options = get_custom_options()
    	
    # This asks the user if they want to save the results of their scan to a file, and if they do, it asks the user what name they want to give to the file
    save = get_save()
    filename = ""
    if save == 1:
        filename = get_filename()
    
    if scan_type == 0:
        display("Custom scan commencing...")
        if save == 0:
            for i in scan_options:
    	        scan(i)
        else:
            for i in scan_options:
                scan_to_file(i, filename)
    elif scan_type == 1:
        display("Light scan commencing...")
        light_scan_options = [0,1,2,4,12,13,14,18,21,23]
        if save == 0:
            for i in light_scan_options:
                scan(i)
        else:
            for i in light_scan_options:
                scan_to_file(i, filename)
    elif scan_type == 2:
        display("Medium scan commencing...")
        medium_scan_options = [0,1,2,3,4,5,6,7,9,10,11,12,13,14,15,18,19,20,21,22,23,24,25,26]
        if save == 0:
            for i in medium_scan_options:
                scan(i)
        else:
            for i in medium_scan_options:
                scan_to_file(i, filename)
    else:
        display("Full scan commencing...")
        full_scan_options = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
        if save == 0:
            for i in full_scan_options:
                scan(i)
        else:
            for i in full_scan_options:
                scan_to_file(i, filename)
    
    display("The scan has been completed")

    # If the scan was saved to a file, this asks the user if they want to send the file to another machine
    if save == 1:
        while get_export() == 1:
            export(filename)
        
        
if __name__=='__main__':
    main()
