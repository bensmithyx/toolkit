from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from subprocess import check_output
import subprocess as sp
import re, os, threading
import socket # for sending the scan file to another machine

class BaseFrame(Frame):
    def __init__(self, master):
    	super().__init__(master)
    	
    	self.header = Frame(self, width = 1024, height = 100)
    	self.main = Frame(self, width = 1024, height = 450)
    	self.footer = Frame(self, width = 1024, height = 50)
    	
    	self.header.grid(row=0, column=0, sticky=N+E)
    	self.header.grid_propagate(False)
    	self.main.grid(row=1, column=0, sticky=N+E)
    	self.main.grid_propagate(False)
    	self.footer.grid(row=2, column=0, sticky=N+E)
    	self.footer.grid_propagate(False)
    	
    	self.printlogo = Canvas(self.header, width = 100, height = 100, highlightthickness = 0)
    	self.printlogo.grid(row=0, column=0, sticky=W)
    	
    	self.img1 = ImageTk.PhotoImage(Image.open("Logo.png"))
    	self.printlogo.create_image(1,1,anchor = N+W, image = self.img1)
    	
    	self.print = Label(self.header, text="CTF MultiTool", fg="#63CCCA", bg="#12263A", font="Raleway 48 bold", pady="10", padx = "0")
    	self.print.grid(row=0, column=1, sticky=N)
    	
    	self.Typeprint = Label(self.main, text="Type of Scan:", fg="#63CCCA", bg="#12263A", font="Raleway 22", pady="10", padx = "0")
    	
    	self.Optionsprint = Label(self.main, text="Options:", fg="#63CCCA", bg="#12263A", font="Raleway 22", pady="10", padx = "0")
    	
    	self.Fileprint = Label(self.main, text="Filename:", fg="#63CCCA", bg="#12263A", font="Raleway 22", pady="10", padx = "0")

    	self.Portprint = Label(self.main, text="Port:", fg="#63CCCA", bg="#12263A", font="Raleway 22", pady="10", padx = "0")

    	self.IPprint = Label(self.main, text="IP Address:", fg="#63CCCA", bg="#12263A", font="Raleway 22", pady="10", padx = "0")

    	
    	self.Typeprint.grid(row = 0, column = 0)
    	self.Optionsprint.grid(row = 0, column = 1)
    	self.Fileprint.grid(row = 0, column = 2)
    	self.Portprint.grid(row = 2, column = 0)
    	self.IPprint.grid(row = 2, column = 1)
    	
    	self.typeentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="5", padx = "5")
    	self.optionsentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="5", padx = "5")
    	self.fileentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="5", padx = "5")
    	self.Portentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="5", padx = "5")
    	self.IPentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="5", padx = "5")
    	self.enumeratebuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="5", padx = "5")
    	
    	self.typeentrybg.grid(row = 1, column = 0)
    	self.optionsentrybg.grid(row = 1, column = 1)
    	self.fileentrybg.grid(row = 1, column = 2, columnspan = 2)
    	self.Portentrybg.grid(row = 3, column = 0)
    	self.IPentrybg.grid(row = 3, column = 1)
    	self.enumeratebuttonbg.grid(row = 3, column = 2, columnspan = 2)
    	
    	self.enumerateoutput = Text(self.main, bg="#12263A", fg='#63CCCA', width = 72, height = 9, borderwidth = 1, relief = SUNKEN, font="Raleway 14")
    	self.enumerateoutput.grid(row = 4, column = 0, columnspan = 3)
    	self.enumerateoutput.config(state = DISABLED)

    	self.outscroll = ttk.Scrollbar(self.main, command=self.enumerateoutput.yview)
    	self.outscroll.grid(row=4, column=2, sticky='nse')
    	self.enumerateoutput['yscrollcommand'] = self.outscroll.set

    	self.v = StringVar()
    	self.Fileentry = ttk.Entry(self.fileentrybg, textvariable = self.v, font="Raleway 22", width = 10)
    	self.Fileentry.grid(row = 0, column = 0)
    	
    	self.x = StringVar()
    	self.Portentry = ttk.Entry(self.Portentrybg, textvariable = self.x, font="Raleway 22", width = 6)
    	self.Portentry.grid(row = 0, column = 0, columnspan = 2)

    	self.y = StringVar()
    	self.IPentry = ttk.Entry(self.IPentrybg, textvariable = self.y, font="Raleway 22", width = 12)
    	self.IPentry.grid(row = 0, column = 0)
    	
    	self.enumeratebutton = ttk.Button(self.enumeratebuttonbg, text = "Enemurate", width = 10, command = self.enumerate_btn_pressed)
    	self.enumeratebutton.grid(row = 0, column = 0)
    	
    	self.typechosen = ttk.Combobox(self.typeentrybg, font="Raleway 22", width = 7)
    	self.typechosen['values'] = ("Custom", "Light", "Medium", "Full")
    	self.typechosen.grid(row = 0, column = 0)		
    	self.typechosen.current()
    	
    	self.optionschosen = ttk.Menubutton(self.optionsentrybg, text="Choose From List ")
    	self.optionschosen.grid(row = 0, column = 0)
    	self.optionschosen.menu = Menu(self.optionschosen, tearoff=0)
    	self.optionschosen["menu"] = self.optionschosen.menu

    	self.option0 = IntVar()
    	self.option1 = IntVar()
    	self.option2 = IntVar()
    	self.option3 = IntVar()
    	self.option4 = IntVar()
    	self.option5 = IntVar()
    	self.option6 = IntVar()
    	self.option7 = IntVar()
    	self.option8 = IntVar()
    	self.option9 = IntVar()
    	self.option10 = IntVar()
    	self.option11 = IntVar()
    	self.option12 = IntVar()
    	self.option13 = IntVar()
    	self.option14 = IntVar()
    	self.option15 = IntVar()
    	self.option16 = IntVar()
    	self.option17 = IntVar()
    	self.option18 = IntVar()
    	self.option19 = IntVar()
    	self.option20 = IntVar()
    	self.option21 = IntVar()
    	self.option22 = IntVar()
    	self.option23 = IntVar()
    	self.option24 = IntVar()
    	self.option25 = IntVar()
    	self.option26 = IntVar()
    	self.option27 = IntVar()
    	self.option28 = IntVar()
    	self.option29 = IntVar()

    	self.optionschosen.menu.add_checkbutton(label="OS information", variable=self.option0)
    	self.optionschosen.menu.add_checkbutton(label="SUDO version", variable=self.option1)
    	self.optionschosen.menu.add_checkbutton(label="Environment variable information", variable=self.option2)
    	self.optionschosen.menu.add_checkbutton(label="Defensive measures information", variable=self.option3)
    	self.optionschosen.menu.add_checkbutton(label="DMESG signature information", variable=self.option4)
    	self.optionschosen.menu.add_checkbutton(label="Device information", variable=self.option5)
    	self.optionschosen.menu.add_checkbutton(label="Cron jobs information", variable=self.option6)
    	self.optionschosen.menu.add_checkbutton(label="Processes information", variable=self.option7)
    	self.optionschosen.menu.add_checkbutton(label="Timers", variable=self.option8)
    	self.optionschosen.menu.add_checkbutton(label="Sockets", variable=self.option9)
    	self.optionschosen.menu.add_checkbutton(label="D-BUS information", variable=self.option10)
    	self.optionschosen.menu.add_checkbutton(label="Network information", variable=self.option11)
    	self.optionschosen.menu.add_checkbutton(label="Information on current user", variable=self.option12)
    	self.optionschosen.menu.add_checkbutton(label="Information on all users", variable=self.option13)
    	self.optionschosen.menu.add_checkbutton(label="SUDO permissions", variable=self.option14)
    	self.optionschosen.menu.add_checkbutton(label="Clipboard and highlighted text", variable=self.option15)
    	self.optionschosen.menu.add_checkbutton(label="PGP keys", variable=self.option16)
    	self.optionschosen.menu.add_checkbutton(label="Common password brute force", variable=self.option17)
    	self.optionschosen.menu.add_checkbutton(label="List of useful binaries", variable=self.option18)
    	self.optionschosen.menu.add_checkbutton(label="Screen and TMUX sessions", variable=self.option19)
    	self.optionschosen.menu.add_checkbutton(label="Root owned SUID/SGID files", variable=self.option20)
    	self.optionschosen.menu.add_checkbutton(label="File permissions of sensitive files", variable=self.option21)
    	self.optionschosen.menu.add_checkbutton(label="Hashes in passwd file", variable=self.option22)
    	self.optionschosen.menu.add_checkbutton(label="Path information", variable=self.option23)
    	self.optionschosen.menu.add_checkbutton(label="Hidden files", variable=self.option24)
    	self.optionschosen.menu.add_checkbutton(label="Log files", variable=self.option25)
    	self.optionschosen.menu.add_checkbutton(label="Writeable files", variable=self.option26)
    	self.optionschosen.menu.add_checkbutton(label="Recently modified files", variable=self.option27)
    	self.optionschosen.menu.add_checkbutton(label="Files containing passwords", variable=self.option28)
    	self.optionschosen.menu.add_checkbutton(label="Files with unexpected ACL", variable=self.option29)

    	self.backbuttonbg = Frame(self.footer, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
    	self.backbuttonbg.grid(row = 0, column = 0, sticky = N+W)
    	
    	self.backbutton = ttk.Button(self.backbuttonbg, text = "Back", width = 6, command = self.back_btn_pressed)
    	self.backbutton.grid(row = 0, column = 0)
    	
    	self.terms = Label(self.footer, text="The company does not take responsibility for any misue of this product.", fg="#63CCCA", bg="#12263A", font="Raleway 16", pady="10")
    	self.terms.grid(row=0, column=1, sticky=N)
    	
    	self.header.configure(background='#12263A')
    	self.printlogo.configure(background='#12263A')
    	self.main.configure(background= '#12263A')
    	self.footer.configure(background='#12263A')
    	
    	sys.stdout = TextRedirector(self.enumerateoutput, "stdout")
    	sys.stderr = TextRedirector(self.enumerateoutput, "stderr")
    	
    	self.pack()

    valid_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    valid_dec = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def scan(self, option_num):
        if option_num == 0: # OS information
            print("OS SYSTEM INFORMATION")
            print(sp.getoutput('(cat /proc/version || uname -a ) 2>/dev/null; lsb_release -a 2>/dev/null'))
        elif option_num == 1: # SUDO version
            print("SUDO VERSION")    
            print(sp.getoutput('sudo -V 2>/dev/null'))
        elif option_num == 2: # Environment variables information
            print("ENVIRONMENT VARIABLES INFORMATION")
            print(sp.getoutput('(env || set) 2>/dev/null'))
        elif option_num == 3: # Defensive measures information
            print("DEFENSIVE MEASURES INFORMATION")    
            print(sp.getoutput('echo AppArmor:'))
            print(sp.getoutput('if [ `which aa-status 2>/dev/null` ]; then aa-status; elif [ `which apparmor_status 2>/dev/null` ]; then apparmor_status; elif ls -d /etc/apparmor* 2>/dev/null; then echo; else echo "Not found AppArmor"; fi'))
            print(sp.getoutput('echo && echo Grsecurity:'))
            print(sp.getoutput('((uname -r | grep "\-grsec" >/dev/null 2>&1 || grep "grsecurity" /etc/sysctl.conf >/dev/null 2>&1) && echo "Yes" || echo "Not found grsecurity")'))
            print(sp.getoutput('echo && echo PaX:'))
            print(sp.getoutput('(which paxctl-ng paxctl >/dev/null 2>&1 && echo "Yes" || echo "Not found PaX")'))
            print(sp.getoutput('echo && echo Execshield:'))
            print(sp.getoutput('(grep "exec-shield" /etc/sysctl.conf || echo "Not found Execshield")'))
            print(sp.getoutput('echo && echo SElinux:'))
            print(sp.getoutput('(sestatus 2>/dev/null || echo "Not found sestatus")'))
            print(sp.getoutput('echo && echo ASLR:'))
            print(sp.getoutput('if [ `cat /proc/sys/kernel/randomize_va_space 2>/dev/null` ]; then if [ `cat /proc/sys/kernel/randomize_va_space 2>/dev/null | grep 1` ]; then echo "Conservative Randomization enabled"; elif [ `cat /proc/sys/kernel/randomize_va_space 2>/dev/null | grep 2` ]; then echo "Full Randomization enabled"; else echo "ASLR disabled"; fi; fi'))
        elif option_num == 4: # Dmesg signature authentication failed
            print("DMESG SIGNATURE INFORMATION")    
            print(sp.getoutput('dmesg 2>/dev/null | grep "signature"'))
        elif option_num == 5: # Drives
            print("DEVICE INFORMATION")    
            print(sp.getoutput('echo Date:'))
            print(sp.getoutput('date 2>/dev/null'))
            print(sp.getoutput('echo && echo System Stats:'))
            print(sp.getoutput('(df -h || lsblk))'))
            print(sp.getoutput('echo && echo CPU:'))
            print(sp.getoutput('lscpu'))
            print(sp.getoutput('echo && echo Printers:'))
            print(sp.getoutput('lpstat -a 2>/dev/null'))
        elif option_num == 6: # Cron jobs belonging to the root user
            print("CRON JOB INFORMATION")
            print(sp.getoutput('crontab -l 2>/dev/null; ls -al /etc/cron* /etc/at* 2>/dev/null; cat /etc/cron* /etc/at* /etc/anacrontab /var/spool/cron/crontabs/root 2>/dev/null | grep -v "^#"'))
        elif option_num == 7: # Running processes belonging to the root user
            print("PROCESSES INFORMATION")    
            print(sp.getoutput('ps aux 2>/dev/null'))
        elif option_num == 8: # Check timers
            print("TIMERS")    
            print(sp.getoutput('systemctl list-timers --all | cat'))
        elif option_num == 9: # Look at sockets
            print("SOCKETS")    
            print(sp.getoutput('netstat -a -p --unix')) #outputs alot of info
        elif option_num == 10: # D-BUS
            print("D-BUS INFORMATION")    
            print(sp.getoutput('busctl list 2>/dev/null'))
        elif option_num == 11: # Network information
            print("NETWORK INFORMATION")
            print(sp.getoutput('echo IP addresses:'))
            print(sp.getoutput('(ip addr show || ifconfig) 2>/dev/null'))
            print(sp.getoutput('echo && echo Ports:'))
            print(sp.getoutput('(ss -auntp || netstat -auntp) 2>/dev/null'))
            print(sp.getoutput('echo && echo Routing:'))
            print(sp.getoutput('(ip route show || route -n) 2>/dev/null'))
            print(sp.getoutput('echo && echo ARP cache:'))
            print(sp.getoutput('(ip neigh show || arp -n) 2>/dev/null'))
        elif option_num == 12: # Current user information
            print("CURRENT USER INFORMATION")    
            print(sp.getoutput('id || (whoami && groups) 2>/dev/null'))
        elif option_num == 13: # All user information
            print("INFORMATION ON ALL USERS")    
            print(sp.getoutput('''cat /etc/passwd | cut -d: -f1; cat /etc/passwd | grep "sh$"; awk -F: '($3 == "0") {print}' /etc/passwd; w; last | tail; lastlog; for i in $(cut -d":" -f1 /etc/passwd 2>/dev/null);do id $i;done 2>/dev/null | sort'''))
        elif option_num == 14: # SUDO permissions
            print("SUDO PERMISSIONS")    
            print(sp.getoutput('sudo -ln 2>/dev/null && sudo -l 2>/dev/null; cat /etc/sudoers 2>/dev/null'))
        elif option_num == 15: # Clipboard and highlighted text
            print("CLIPBOARD AND HIGHLIGHTED TEXT")    
            print(sp.getoutput('if [ `which xclip 2>/dev/null` ]; then echo "Clipboard: "`xclip -o -selection clipboard 2>/dev/null`; echo "Highlighted text: "`xclip -o 2>/dev/null`; elif [ `which xsel 2>/dev/null` ]; then echo "Clipboard: "`xsel -ob 2>/dev/null`; echo "Highlighted text: "`xsel -o 2>/dev/null`; else echo "Not found xsel and xclip"; fi'))
        elif option_num == 16: # PGP keys
            print("PGP KEYS")    
            print(sp.getoutput('gpg --list-keys 2>/dev/null'))
        elif option_num == 17: # Common password list brute force
            print("COMMON PASSWORD BRUTE FORCE")
            try:
                password_file = open("password_list.txt", "r")
                for line in password_file:
                    print(sp.getoutput('echo %s | timeout 0.25 sudo -kS echo "Password found: %s" 2>/dev/null' % (line.strip(), line.strip())))
                password_file.close()
            except OSError:
                print("Error, brute force password list not found!")
        elif option_num == 18: # Useful binaries list
            print("USEFUL BINARIES")    
            print(sp.getoutput('which nmap aws nc ncat netcat nc.traditional wget curl ping gcc g++ make gdb base64 socat python python2 python3 python2.7 python2.6 python3.6 python3.7 perl php ruby xterm doas sudo fetch docker lxc ctr runc rkt kubectl 2>/dev/null'))
        elif option_num == 19: # Screen and TMUX sessions
            print("SCREEN AND TMUX SESSIONS")    
            print(sp.getoutput('echo Screen:'))
            print(sp.getoutput('if [ `which screen 2>/dev/null` ]; then (screen -ls); else echo "Screen not found"; fi'))
            print(sp.getoutput('echo && echo Tmux:'))
            print(sp.getoutput('if [ `which tmux 2>/dev/null` ]; then (tmux ls); else echo "Tmux not found"; fi'))
        elif option_num == 20: # Files with SUID or SGID bits set
            print("FILES WITH SUID SET")    
            print(sp.getoutput('find / -perm -4000 2>/dev/null'))
            print("FILES WITH SGID SET")
            print(sp.getoutput('find / -perm -2000 2>/dev/null'))
        elif option_num == 21: # File permissions of sensitive files
            print("FILE PERMISSIONS FOR SENSITIVE FILES")    
            print(sp.getoutput('ls -l /etc/passwd 2>/dev/null; ls -l /etc/shadow 2>/dev/null'))
        elif option_num == 22: # Looking for hashes in /etc/passwd
            print("HASHES IN PASSWD FILE")    
            print(sp.getoutput('echo Passwd equivalent files:'))
            print(sp.getoutput('cat /etc/passwd /etc/pwd.db /etc/master.passwd /etc/group 2>/dev/null'))
            print(sp.getoutput('echo && echo Shadow equivalent files:'))
            print(sp.getoutput('cat /etc/shadow /etc/shadow- /etc/shadow~ /etc/gshadow /etc/gshadow- /etc/master.passwd /etc/spwd.db /etc/security/opasswd 2>/dev/null'))
            print(sp.getoutput('echo && echo Password hashes:'))
            print(sp.getoutput("grep -v '^[^:]*:[x\*]' /etc/passwd /etc/pwd.db /etc/master.passwd /etc/group 2>/dev/null"))
        elif option_num == 23: # Path information
            print("PATH INFORMATION")    
            print(sp.getoutput('echo $PATH 2>/dev/null'))
        elif option_num == 24: # List of hidden files
            print("HIDDEN FILES")    
            print(sp.getoutput('find / -type f -iname ".*" -ls 2>/dev/null'))
        elif option_num == 25: # Log files
            print("LOG FILES")    
            print(sp.getoutput('''if [ `which aureport 2>/dev/null` ]; then (aureport --tty 2>/dev/null | grep -E "su |sudo "; grep -RE 'comm="su"|comm="sudo"' /var/log* 2>/dev/null); else echo "To view log file information, please install 'aureport'"; fi'''))
        elif option_num == 26: # List of writeable files
            print("WRITEABLE FILES") 
            # finds files owned by the user or that  are world writeable   
            print(sp.getoutput("find / '(' -type f -or -type d ')' '(' '(' -user $USER ')' -or '(' -perm -o=w ')' ')' 2>/dev/null | grep -v '/proc/' | grep -v $HOME | sort | uniq"))
            # finds files that are writeable by any group of the user
            print(sp.getoutput("for g in `groups`; do find \( -type f -or -type d \) -group $g -perm -g=w 2>/dev/null | grep -v '/proc/' | grep -v $HOME; done"))
        elif option_num == 27: # List of recently modified files
            print("RECENTLY MODIFIED FILES")    
            print(sp.getoutput('find / -type f -mmin -5 ! -path "/proc/*" ! -path "/sys/*" ! -path "/run/*" ! -path "/dev/*" ! -path "/var/lib/*" 2>/dev/null'))
        elif option_num == 28: # Searching files that contain passwords
            print("FILES CONTAINING PASSWORDS")    
            print(sp.getoutput('''intpwdfiles=`timeout 150 grep -RiIE "(pwd|passwd|password|PASSWD|PASSWORD|dbuser|dbpass).*[=:].+|define ?\('(\w*passw|\w*user|\w*datab)" $HOMESEARCH /var/www /usr/local/www/ $backup_folders_row /tmp /etc /root /mnt /Users /private 2>/dev/null`; printf "%s\n" "$intpwdfiles" | grep -I ".php:"| sort | uniq | head -n 70; printf "%s\n" "$intpwdfiles" | grep -vI ".php:" | grep -E "^/" | grep ":"| sort | uniq | head -n 70'''))
        elif option_num == 29: # Unexpected ACL
            print("FILES WITH AN ACL")    
            print(sp.getoutput('getfacl -t -s -R -p /bin /etc /home /opt /root /sbin /usr /tmp 2>/dev/null'))

    def title_in_file(self, name, filename):
        os.system('echo >> %s' % (filename))
        os.system('(%s %s %s) >> %s' % ("echo '########## ", str(name), " ##########'", filename))
        os.system('echo >> %s' % (filename))

    def scan_to_file(self, option_num, filename):
        if option_num == 0: # OS information
            self.title_in_file("OS SYSTEM INFORMATION", filename)
            os.system('((cat /proc/version || uname -a ) 2>/dev/null; lsb_release -a 2>/dev/null) >> %s' % (filename))
        elif option_num == 1: # SUDO version
            self.title_in_file("SUDO VERSION", filename)    
            os.system('(sudo -V 2>/dev/null) >> %s' % (filename))
        elif option_num == 2: # Environment variables information
            self.title_in_file("ENVIRONMENT VARIABLES INFORMATION", filename) 
            os.system('((env || set) 2>/dev/null) >> %s' % (filename))
        elif option_num == 3: # Defensive measures information
            self.title_in_file("DEFENSIVE MEASURES INFORMATION", filename)     
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
            self.title_in_file("DMESG SIGNATURE INFORMATION", filename) 
            os.system('(dmesg 2>/dev/null | grep "signature") >> %s' % (filename))
        elif option_num == 5: # Drives
            self.title_in_file("DEVICE INFORMATION", filename) 
            os.system('(echo Date:) >> %s' % (filename))
            os.system('(date 2>/dev/null) >> %s' % (filename))
            os.system('(echo && echo System Stats:) >> %s' % (filename))
            os.system('(df -h || lsblk) >> %s' % (filename))
            os.system('(echo && echo CPU:) >> %s' % (filename))
            os.system('(lscpu) >> %s' % (filename))
            os.system('(echo && echo Printers:) >> %s' % (filename))
            os.system('(lpstat -a 2>/dev/null) >> %s' % (filename))
        elif option_num == 6: # Cron jobs belonging to the root user
            self.title_in_file("CRON JOB INFORMATION", filename) 
            os.system('(crontab -l 2>/dev/null; ls -al /etc/cron* /etc/at* 2>/dev/null; cat /etc/cron* /etc/at* /etc/anacrontab /var/spool/cron/crontabs/root 2>/dev/null | grep -v "^#") >> %s' % (filename))
        elif option_num == 7: # Running processes belonging to the root user
            self.title_in_file("PROCESSES INFORMATION", filename) 
            os.system('(ps aux 2>/dev/null) >> %s' % (filename))
        elif option_num == 8: # Check timers
            self.title_in_file("TIMERS", filename) 
            os.system('(systemctl list-timers --all | cat) >> %s' % (filename))
        elif option_num == 9: # Look at sockets
            self.title_in_file("SOCKETS", filename) 
            os.system('(netstat -a -p --unix) >> %s' % (filename)) #outputs alot of info
        elif option_num == 10: # D-BUS
            self.title_in_file("D-BUS INFORMATION", filename) 
            os.system('(busctl list 2>/dev/null) >> %s' % (filename))
        elif option_num == 11: # Network information
            self.title_in_file("NETWORK INFORMATION", filename) 
            os.system('(echo IP addresses:) >> %s' % (filename))
            os.system('((ip addr show || ifconfig) 2>/dev/null) >> %s' % (filename))
            os.system('(echo && echo Ports:) >> %s' % (filename))
            os.system('((ss -auntp || netstat -auntp) 2>/dev/null) >> %s' % (filename))
            os.system('(echo && echo Routing:) >> %s' % (filename))
            os.system('((ip route show || route -n) 2>/dev/null) >> %s' % (filename))
            os.system('(echo && echo ARP cache:) >> %s' % (filename))
            os.system('((ip neigh show || arp -n) 2>/dev/null) >> %s' % (filename))
        elif option_num == 12: # Current user information
            self.title_in_file("CURRENT USER INFORMATION", filename) 
            os.system('(id || (whoami && groups) 2>/dev/null) >> %s' % (filename))
        elif option_num == 13: # All user information
            self.title_in_file("INFORMATION ON ALL USERS", filename) 
            os.system('''(cat /etc/passwd | cut -d: -f1; cat /etc/passwd | grep "sh$"; awk -F: '($3 == "0") {print}' /etc/passwd; w; last | tail; lastlog; for i in $(cut -d":" -f1 /etc/passwd 2>/dev/null);do id $i;done 2>/dev/null | sort) >> %s''' % (filename))
        elif option_num == 14: # SUDO permissions
            self.title_in_file("SUDO PERMISSIONS", filename)
            os.system('(sudo -ln 2>/dev/null && sudo -l 2>/dev/null; cat /etc/sudoers 2>/dev/null) >> %s' % (filename))
        elif option_num == 15: # Clipboard and highlighted text
            self.title_in_file("CLIPBOARD AND HIGHLIGHTED TEXT", filename) 
            os.system('(if [ `which xclip 2>/dev/null` ]; then echo "Clipboard: "`xclip -o -selection clipboard 2>/dev/null`; echo "Highlighted text: "`xclip -o 2>/dev/null`; elif [ `which xsel 2>/dev/null` ]; then echo "Clipboard: "`xsel -ob 2>/dev/null`; echo "Highlighted text: "`xsel -o 2>/dev/null`; else echo "Not found xsel and xclip"; fi) >> %s' % (filename))
        elif option_num == 16: # PGP keys
            self.title_in_file("PGP KEYS", filename) 
            os.system('(gpg --list-keys 2>/dev/null) >> %s' % (filename))
        elif option_num == 17: # Common password list brute force
            self.title_in_file("COMMON PASSWORD BRUTE FORCE")
            try:
                password_file = open("password_list.txt", "r")
                for line in password_file:
                    os.system('(echo %s | timeout 0.25 sudo -kS echo "Password found: %s" 2>/dev/null) >> %s' % (line.strip(), line.strip(), filename))
                password_file.close()
            except OSError:
                print("Error, brute force password list not found!")
        elif option_num == 18: # Useful binaries list
            self.title_in_file("USEFUL BINARIES", filename) 
            os.system('(which nmap aws nc ncat netcat nc.traditional wget curl ping gcc g++ make gdb base64 socat python python2 python3 python2.7 python2.6 python3.6 python3.7 perl php ruby xterm doas sudo fetch docker lxc ctr runc rkt kubectl 2>/dev/null) >> %s' % (filename))
        elif option_num == 19: # Screen and TMUX sessions
            self.title_in_file("SCREEN AND TMUX SESSIONS", filename) 
            os.system('(echo Screen:) >> %s' % (filename))
            os.system('(if [ `which screen 2>/dev/null` ]; then (screen -ls); else echo "Screen not found"; fi) >> %s' % (filename))
            os.system('(echo && echo Tmux:) >> %s' % (filename))
            os.system('(if [ `which tmux 2>/dev/null` ]; then (tmux ls); else echo "Tmux not found"; fi) >> %s' % (filename))
        elif option_num == 20: # Root owned files with SUID or SGID bits set
            self.title_in_file("FILES WITH SUID SET", filename)    
            os.system('(find / -perm -4000 2>/dev/null) >> %s' % (filename))
            self.title_in_file("FILES WITH SGID SET", filename) 
            os.system('(find / -perm -2000 2>/dev/null) >> %s' % (filename))
        elif option_num == 21: # File permissions of sensitive files
            self.title_in_file("FILE PERMISSIONS FOR SENSITIVE FILES", filename) 
            os.system('(ls -l /etc/passwd 2>/dev/null; ls -l /etc/shadow 2>/dev/null) >> %s' % (filename))
        elif option_num == 22: # Looking for hashes in /etc/passwd
            self.title_in_file("HASHES IN PASSWD FILE", filename) 
            os.system('(echo Passwd equivalent files:) >> %s' % (filename))
            os.system('(cat /etc/passwd /etc/pwd.db /etc/master.passwd /etc/group 2>/dev/null) >> %s' % (filename))
            os.system('(echo && echo Shadow equivalent files:) >> %s' % (filename))
            os.system('(cat /etc/shadow /etc/shadow- /etc/shadow~ /etc/gshadow /etc/gshadow- /etc/master.passwd /etc/spwd.db /etc/security/opasswd 2>/dev/null) >> %s' % (filename))
            os.system('(echo && echo Password hashes:) >> %s' % (filename))
            os.system("(grep -v '^[^:]*:[x\*]' /etc/passwd /etc/pwd.db /etc/master.passwd /etc/group 2>/dev/null) >> %s" % (filename))
        elif option_num == 23: # Path information
            self.title_in_file("PATH INFORMATION", filename) 
            os.system('(echo $PATH 2>/dev/null) >> %s' % (filename))
        elif option_num == 24: # List of hidden files
            self.title_in_file("HIDDEN FILES", filename) 
            os.system('(find / -type f -iname ".*" -ls 2>/dev/null) >> %s' % (filename))
        elif option_num == 25: # Log files
            self.title_in_file("LOG FILES", filename) 
            os.system('''(if [ `which aureport 2>/dev/null` ]; then (aureport --tty 2>/dev/null | grep -E "su |sudo "; grep -RE 'comm="su"|comm="sudo"' /var/log* 2>/dev/null); else echo "To view log file information, please install 'aureport'"; fi) >> %s''' % (filename))
        elif option_num == 26: # List of writeable files
            self.title_in_file("WRITEABLE FILES", filename) 
            # finds files owned by the user or that  are world writeable
            os.system("(find / '(' -type f -or -type d ')' '(' '(' -user $USER ')' -or '(' -perm -o=w ')' ')' 2>/dev/null | grep -v '/proc/' | grep -v $HOME | sort | uniq) >> %s" % (filename))
            # finds files that are writeable by any group of the user
            os.system("(for g in `groups`; do find \( -type f -or -type d \) -group $g -perm -g=w 2>/dev/null | grep -v '/proc/' | grep -v $HOME; done) >> %s" % (filename))
        elif option_num == 27: # List of recently modified files
            self.title_in_file("RECENTLY MODIFIED FILES", filename) 
            os.system('(find / -type f -mmin -5 ! -path "/proc/*" ! -path "/sys/*" ! -path "/run/*" ! -path "/dev/*" ! -path "/var/lib/*" 2>/dev/null) >> %s' % (filename))
        elif option_num == 28: # Searching files that contain passwords
            self.title_in_file("FILES CONTAINING PASSWORDS", filename) 
            os.system(f'''(intpwdfiles=`timeout 150 grep -RiIE "(pwd|passwd|password|PASSWD|PASSWORD|dbuser|dbpass).*[=:].+|define ?\('(\w*passw|\w*user|\w*datab)" $HOMESEARCH /var/www /usr/local/www/ $backup_folders_row /tmp /etc /root /mnt /Users /private 2>/dev/null`; printf "%s\n" "$intpwdfiles" | grep -I ".php:"| sort | uniq | head -n 70; printf "%s\n" "$intpwdfiles" | grep -vI ".php:" | grep -E "^/" | grep ":"| sort | uniq | head -n 70) >> {filename}''')
        elif option_num == 29: # ACL
            self.title_in_file("FILES WITH AN ACL", filename) 
            os.system('(getfacl -t -s -R -p /bin /etc /home /opt /root /sbin /usr /tmp 2>/dev/null) >> %s' % (filename))

    def checkIP(self, ip):
        if ip == "":
            return 1
        ip = ip.split(".")
        if len(ip) == 4:
            for x in range(0, len(ip)):
                for y in ip[x]:
                    if y not in self.valid_dec:
                        return 0
                    if ip[x] == "0" and (x == 1 or x == 2):
                        pass
                    elif ip[x][0] == "0":
                        ip[x] = ip[x][1:]
                if ip[x] == '':
                    return 0
                if int(ip[x]) > 255:
                    return 0
            return ip[0] + "." + ip[1] + "." +  ip[2] + "." + ip[3]
        else:
            return 0

    def scanall(self, numbers, valid, filename):
        if valid == False:
            for i in numbers:
                self.scan(i)
        else:
            for i in numbers:
                self.scan_to_file(i, filename)
        print("The scan has been completed")
            
        
        
    def enumerate_btn_pressed(self):
        scantype = self.typechosen.get()
        filename = self.Fileentry.get()
        port = self.Portentry.get()
        userip = self.IPentry.get()
        valid_filename = False
        valid_for_export = False
        valid = False

        ip = self.checkIP(userip)
        if ip != 0:
            if str(port) == "":
                if filename != "":
                    if len(re.findall("[A-Za-z0-9_.]", filename)) != len(filename):
                        messagebox.showerror(title="ERROR!!!", message="Please Choose a Valid Filename!")
                    else:
                        try:
                            f = open(filename,"x")
                        except FileExistsError:
                            messagebox.showerror(title="ERROR!!!", message="File Already Exists. Please Choose a Valid Filename!")
                        except:
                            messagebox.showerror(title="ERROR!!!", message="Please Choose a Valid Filename!")
                        else:
                            f.close()
                            valid_filename = True
                            valid = True
                else:
                    valid = True
            else:
                try:   
                    if int(port) in range(65536): 
                        if filename != "":
                            if len(re.findall("[A-Za-z0-9_.]", filename)) != len(filename):
                                messagebox.showerror(title="ERROR!!!", message="Please Choose a Valid Filename!")
                            else:
                                try:
                                    f = open(filename,"x")
                                except FileExistsError:
                                    messagebox.showerror(title="ERROR!!!", message="File Already Exists. Please Choose a Valid Filename!")
                                except:
                                    messagebox.showerror(title="ERROR!!!", message="Please Choose a Valid Filename!")
                                else:
                                    f.close()
                                    valid_filename = True
                                    valid_for_export = True
                                    valid = True
                        else:
                            valid = True
                    else:
                        messagebox.showerror(title="ERROR!!!", message="Please Choose a Valid Port!")
                except:
                    messagebox.showerror(title="ERROR!!!", message="Please Choose a Valid Port!")
        
        else:
            messagebox.showerror(title="ERROR!!!", message="Please Choose a Valid IP Address!")
            

        if valid == True:
            if scantype.lower() == "custom":
                scan_options = []
                print("Custom scan commencing...")
                if self.option0.get() == True:
                    scan_options.append(0)
                if self.option1.get() == True:
                    scan_options.append(1)
                if self.option2.get() == True:
                    scan_options.append(2)
                if self.option3.get() == True:
                    scan_options.append(3)
                if self.option4.get() == True:
                    scan_options.append(4)
                if self.option5.get() == True:
                    scan_options.append(5)
                if self.option6.get() == True:
                    scan_options.append(6)
                if self.option7.get() == True:
                    scan_options.append(7)
                if self.option8.get() == True:
                    scan_options.append(8)
                if self.option9.get() == True:
                    scan_options.append(9)
                if self.option10.get() == True:
                    scan_options.append(10)
                if self.option11.get() == True:
                    scan_options.append(11)
                if self.option12.get() == True:
                    scan_options.append(12)
                if self.option13.get() == True:
                    scan_options.append(13)
                if self.option14.get() == True:
                    scan_options.append(14)
                if self.option15.get() == True:
                    scan_options.append(15)
                if self.option16.get() == True:
                    scan_options.append(16)
                if self.option17.get() == True:
                    scan_options.append(17)
                if self.option18.get() == True:
                    scan_options.append(18)
                if self.option19.get() == True:
                    scan_options.append(19)
                if self.option20.get() == True:
                    scan_options.append(20)
                if self.option21.get() == True:
                    scan_options.append(21)
                if self.option22.get() == True:
                    scan_options.append(22)
                if self.option23.get() == True:
                    scan_options.append(23)
                if self.option24.get() == True:
                    scan_options.append(24)
                if self.option25.get() == True:
                    scan_options.append(25)
                if self.option26.get() == True:
                    scan_options.append(26)
                if self.option27.get() == True:
                    scan_options.append(27)
                if self.option28.get() == True:
                    scan_options.append(28)
                if self.option29.get() == True:
                    scan_options.append(29)

                threading._start_new_thread(self.scanall, (scan_options, valid_filename, filename))
                messagebox.showinfo(title="SUCCESS!!!", message=scantype + " Scan is Now Being Conducted!")
                        
            elif scantype.lower() == "light":
                print("Light scan commencing...")
                light_scan_options = [0,1,2,4,12,13,14,18,21,23]
                threading._start_new_thread(self.scanall, (light_scan_options, valid_filename, filename))
                messagebox.showinfo(title="SUCCESS!!!", message=scantype + " Scan is Now Being Conducted!")
                        
            elif scantype.lower() == "medium":
                print("Medium scan commencing...")
                medium_scan_options = [0,1,2,3,4,5,6,7,9,10,11,12,13,14,15,18,19,20,21,22,23,24,25,26]
                threading._start_new_thread(self.scanall, (medium_scan_options, valid_filename, filename))
                messagebox.showinfo(title="SUCCESS!!!", message=scantype + " Scan is Now Being Conducted!")
                        
            elif scantype.lower() == "full":
                print("Full scan commencing...")
                full_scan_options = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
                threading._start_new_thread(self.scanall, (full_scan_options, valid_filename, filename))
                messagebox.showinfo(title="SUCCESS!!!", message=scantype + " Scan is Now Being Conducted!")

            else:
                messagebox.showerror(title="ERROR!!!", message="Please Chose a Valid Type of Scan!")
                
            if valid_for_export == True:
                try:
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.connect((userip, int(port)))
                    try:
                        f = open(filename, 'rb')
                        scan_text = f.read(1024)
                        while(scan_text):
                            client_socket.send(scan_text)
                            scan_text = f.read()
                        f.close()
                    except OSError:
                        messagebox.showerror(title="ERROR!!!", message="Scan File Not Found!")
                    client_socket.close()
                except OSError:
                    messagebox.showerror(title="ERROR!!!", message="Connection Failed!!")
    	
    def back_btn_pressed(self):
    	root.destroy()
    	import MainMenu

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
    

root = Tk()
root.option_add("*TCombobox*Listbox*Background", '#12263A')
root.option_add("*TCombobox*Listbox*Foreground", '#63CCCA')
root.option_add("*TCombobox*Listbox*Font", 'Raleway 17')

root.option_add("*TMenubutton*Listbox*Background", '#12263A')
root.option_add("*TMenubutton*Listbox*Foreground", '#63CCCA')
root.option_add("*TMenubutton*Listbox*Font", 'Raleway 17')

wmgstyle = ttk.Style()
wmgstyle.theme_create('wmgstyle', parent = 'alt', settings = {'TCombobox': {'configure': {'fieldbackground': '#63CCCA', 'background': '#12263A', 'foreground': '#12263A', 'arrowcolor': "#63CCCA" , 'arrowsize' : '20', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TEntry': {'configure': {'fieldbackground': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TButton': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA", 'font': "Raleway 21"}}, 'TScrollbar': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA"}}, 'TMenubutton': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'activebackground' : '#12263A', 'activeforeground' : "#63CCCA",'fieldbackground': '#63CCCA', 'font': "Raleway 21", 'arrowcolor': "#12263A" , 'arrowsize' : '5'}}})

wmgstyle.theme_use("wmgstyle")

lf = BaseFrame(root)
root.geometry("1024x600")
root.title("CTF Toolkit")
root.iconphoto(False, PhotoImage(file="Icon.png"))
root.resizable(False, False)
root.mainloop()
