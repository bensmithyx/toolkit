from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from subprocess import check_output
import subprocess
import re
import sys
import os,time

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")

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
    	
    	self.titlelogo = Canvas(self.header, width = 100, height = 100, highlightthickness = 0)
    	self.titlelogo.grid(row=0, column=0, sticky=W)
    	
    	self.img1 = ImageTk.PhotoImage(Image.open("Logo.png"))
    	self.titlelogo.create_image(1,1,anchor = N+W, image = self.img1)
    	
    	self.title = Label(self.header, text="CTF MultiTool", fg="#63CCCA", bg="#12263A", font="Raleway 48 bold", pady="10", padx = "20")
    	self.title.grid(row=0, column=1, sticky=N)
    	
    	self.Languagetitle = Label(self.main, text="Language:", fg="#63CCCA", bg="#12263A", font="Raleway 24", pady="10", padx = "20")
    	
    	self.IPtitle = Label(self.main, text="IP Address:", fg="#63CCCA", bg="#12263A", font="Raleway 24", pady="10", padx = "20")
    	
    	self.Porttitle = Label(self.main, text="Port:", fg="#63CCCA", bg="#12263A", font="Raleway 24", pady="10", padx = "20")
    	
    	self.Languagetitle.grid(row = 0, column = 0)
    	self.IPtitle.grid(row = 0, column = 1)
    	self.Porttitle.grid(row = 0, column = 2)
    	
    	self.languageentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")
    	self.IPentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")
    	self.Portentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")
    	self.reversebuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")
    	
    	self.languageentrybg.grid(row = 1, column = 0)
    	self.IPentrybg.grid(row = 1, column = 1)
    	self.Portentrybg.grid(row = 1, column = 2)
    	self.reversebuttonbg.grid(row = 1, column = 3, columnspan = 2)
    	
    	self.reverseoutput = Text(self.main, bg="#12263A", fg='#63CCCA', width = 72, height = 10, borderwidth = 1, relief = SUNKEN, font="Raleway 14")
    	self.reverseoutput.grid(row = 2, column = 0, columnspan = 4)
    	self.reverseoutput.config(state = DISABLED)

    	self.outscroll = ttk.Scrollbar(self.main, command=self.reverseoutput.yview)
    	self.outscroll.grid(row=2, column=3, sticky='nse')
    	self.reverseoutput['yscrollcommand'] = self.outscroll.set
    	
    	self.v = StringVar()
    	self.Portentry = ttk.Entry(self.Portentrybg, textvariable = self.v, font="Raleway 24", width = 6)
    	self.Portentry.grid(row = 0, column = 0)
    	
    	self.reversebutton = ttk.Button(self.reversebuttonbg, text = "Exploit", width = 6, command = self.attack_btn_pressed)
    	self.reversebutton.grid(row = 0, column = 0)
    	
    	self.languagechosen = ttk.Combobox(self.languageentrybg, font="Raleway 24", width = 11)
    	self.languagechosen['values'] = ("Bash","Perl","Python","PHP","Ruby","Golang","Netcat","Ncat","Powershell","TCLsh","Gawk","Telnet")
    	self.languagechosen.grid(row = 0, column = 0)		
    	self.languagechosen.current()

    	self.ipchosen = ttk.Combobox(self.IPentrybg, font="Raleway 24", width = 12)
    	self.ipchosen['values'] = self.get_ip()
    	self.ipchosen.grid(row = 0, column = 0)		
    	self.ipchosen.current()

    	self.backbuttonbg = Frame(self.footer, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
    	self.backbuttonbg.grid(row = 0, column = 0, sticky = N+W)
    	
    	self.backbutton = ttk.Button(self.backbuttonbg, text = "Back", width = 6, command = self.back_btn_pressed)
    	self.backbutton.grid(row = 0, column = 0)
    	
    	self.terms = Label(self.footer, text="The company does not take responsibility for any misue of this product.", fg="#63CCCA", bg="#12263A", font="Raleway 16", pady="10")
    	self.terms.grid(row=0, column=1, sticky=N)
    	
    	self.header.configure(background='#12263A')
    	self.titlelogo.configure(background='#12263A')
    	self.main.configure(background= '#12263A')
    	self.footer.configure(background='#12263A')
    	
    	sys.stdout = TextRedirector(self.reverseoutput, "stdout")
    	sys.stderr = TextRedirector(self.reverseoutput, "stderr")
    	
    	self.pack()

    #def run_listener(self,command):
    #    

    def get_ip(self):
        list_ips = []
        valid_ips = 0
        ips = check_output(['hostname', '--all-ip-addresses']).decode("utf-8").split()
        for index, ip in enumerate(ips):
            pattern = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
            test = pattern.match(ip)
            if test:
                valid_ips +=1
                list_ips.append(ip)
        return list_ips
        
    def OutputCommands(self, ip, port, language): 
        file1 = open('reversescripts.txt','r+')
        lines = file1.readlines()
        codeno = 0
        for line in lines:
            for i in line.strip():
                if i == '@':
                    line = line.replace("@",ip)
                elif i == '£':
                    line = line.replace("£",str(port))

            langArr = [["bash-","bash1-"],["perl-","perl1-","perl2-"],["python-","python1-","python2-"],["php-","php1-","php2-","php3-","php4-","php5-"],["ruby-","ruby1-"],["golang-"],["netcatbsd-","netcattrad-","netcattrad1-"],["ncat-"],["powershell-","powershell1-"],["tclsh-"],["gawk-"],["telnet-","telnet1-"]]

            numofoutputs = len(langArr[language])
            
            for j in langArr[language]: #for each revereshell script relating to the language
                if j in line.strip(): #find the code which relates to the strings in langArr
                    codeno += 1

        for x in range(0, codeno):
            shellcode = x
            linecount = 0 #set linecount to 0
            
            for line in lines: #for each line in file
                linecount += 1 #increment linecount to signify which line we are on
                if langArr[language][shellcode] in line:
                    line = line.replace("@",ip) #replace ip and port again for that specific code chosen
                    line = line.replace("£",str(port))
                    line = line.replace(langArr[language][shellcode],"")
                    print("Copy this and paste into the victim machine:\n" + line) #output code to copy
                    lines[linecount] = lines[linecount].replace("@",ip)
                    lines[linecount] = lines[linecount].replace("£",str(port))
                    break #break da loop so we can end
            file1.close() #close files
        return str(lines[linecount])
        


    def attack_btn_pressed(self):
        language = self.languagechosen.get()
        ip = self.ipchosen.get()
        port = self.Portentry.get()
        languages = ["bash","perl","python","php","ruby","golang","netcat","ncat","powershell","tclsh","gawk","telnet"]
        if language.lower() in languages:
            languageid = languages.index(language.lower())
            if ip in self.get_ip():
                try:
                    port = int(port)
                except:
                    messagebox.showerror(title="ERROR!!!", message="The Port " + str(port) + " is not Valid!")
                else:
                    if int(port) in range(1,65536):
                        messagebox.showinfo(title="SUCCESS!!!", message="Exploit is Now Being Conducted!")
                        command = self.OutputCommands(ip, port, languageid)
                        command2 = "xterm -hold -e " +  command
                        os.system(command2)

                    else:
                        messagebox.showerror(title="ERROR!!!", message="The Port " + str(port) + " is not Valid!")
            else:
                messagebox.showerror(title="ERROR!!!", message="The IP Address " + str(ip) + " is not Valid!")
        else:
            messagebox.showerror(title="ERROR!!!", message="The Language " + str(language) + " is not Valid!")
    	
    def back_btn_pressed(self):
    	root.destroy()
    	import MainMenu
    

root = Tk()
root.option_add("*TCombobox*Listbox*Background", '#12263A')
root.option_add("*TCombobox*Listbox*Foreground", '#63CCCA')
root.option_add("*TCombobox*Listbox*Font", 'Raleway 17')

wmgstyle = ttk.Style()
wmgstyle.theme_create('wmgstyle', parent = 'alt', settings = {'TCombobox': {'configure': {'fieldbackground': '#63CCCA', 'background': '#12263A', 'foreground': '#12263A', 'arrowcolor': "#63CCCA" , 'arrowsize' : '20', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TEntry': {'configure': {'fieldbackground': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TButton': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA", 'font': "Raleway 21"}}, 'TScrollbar': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA"}}})

wmgstyle.theme_use("wmgstyle")

lf = BaseFrame(root)
root.geometry("1024x600")
root.title("CTF Toolkit")
root.iconphoto(False, PhotoImage(file="Icon.png"))
root.resizable(False, False)
root.mainloop()

