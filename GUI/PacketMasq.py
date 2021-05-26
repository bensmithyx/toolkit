from tkinter import *
from tkinter import ttk
#import tkinter.messagebox as tm
from tkinter import messagebox
from scapy.all import *
import sys
from PIL import ImageTk, Image

class TextRedirector(object): #Text redirector redirecting anything from stdout to the tkinter text box for GUI output
	def __init__(self, widget, tag="stdout"):
		self.widget = widget
		self.tag = tag

	def write(self, str):
		self.widget.configure(state="normal")
		self.widget.insert("end", str, (self.tag,))
		self.widget.configure(state="disabled")

class BaseFrame(Frame): # setting up base frame for our tkinter window
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
		self.footer.grid_propagate(False)                              # setting up layout and buttons etc V
		
		self.titlelogo = Canvas(self.header, width = 100, height = 100, highlightthickness = 0)
		self.titlelogo.grid(row=0, column=0, sticky=W)
		
		self.img1 = ImageTk.PhotoImage(Image.open("Logo.png"))
		self.titlelogo.create_image(1,1,anchor = N+W, image = self.img1)
		
		self.title = Label(self.header, text="CTF MultiTool", fg="#63CCCA", bg="#12263A", font="Raleway 48 bold", pady="10", padx = "20")
		self.title.grid(row=0, column=1, sticky=N)
		
		self.Typetitle = Label(self.main, text="Packet type:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.Typetitle.grid(row=0, column=0, sticky=W)
		
		self.typechosen = ttk.Combobox(self.main, font="Raleway 18", width = 17)
		self.typechosen['values'] = ('ICMP', 'TCP', 'UDP')
		self.typechosen.grid(row = 0, column = 1)		
		self.typechosen.current()
		
		
		self.SMactitle = Label(self.main, text="Source Mac Address:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.SMactitle.grid(row=1, column=0, sticky=W)
		
		self.a = StringVar()
		self.SMacEntry = ttk.Entry(self.main, textvariable = self.a, font="Raleway 18", width = 18)
		self.SMacEntry.grid(row = 1, column = 1)
		
		self.SIPtitle = Label(self.main, text="Source IP Address:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.SIPtitle.grid(row=2, column=0, sticky=W)
		
		self.b = StringVar()
		self.SIPEntry = ttk.Entry(self.main, textvariable = self.b, font="Raleway 18", width = 18)
		self.SIPEntry.grid(row = 2, column = 1)
		
		self.DIPtitle = Label(self.main, text="Destination IP Address:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.DIPtitle.grid(row=3, column=0, sticky=W)
		
		self.c = StringVar()
		self.DIPEntry = ttk.Entry(self.main, textvariable = self.c, font="Raleway 18", width = 18)
		self.DIPEntry.grid(row = 3, column = 1)
		
		self.SPorttitle = Label(self.main, text="Source port:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.SPorttitle.grid(row=4, column=0, sticky=W)
		
		self.d= StringVar()
		self.SPortEntry = ttk.Entry(self.main, textvariable = self.d, font="Raleway 18", width = 18)
		self.SPortEntry.grid(row = 4, column = 1)
		
		self.DPorttitle = Label(self.main, text="Destination port:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.DPorttitle.grid(row=5, column=0, sticky=W)
		
		self.e= StringVar()
		self.DPortEntry = ttk.Entry(self.main, textvariable = self.e, font="Raleway 18", width = 18)
		self.DPortEntry.grid(row = 5, column = 1)
		
		self.PacketIDtitle = Label(self.main, text="Packet ID:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.PacketIDtitle.grid(row=6, column=0, sticky=W)
		
		self.f= StringVar()
		self.PacketIDEntry = ttk.Entry(self.main, textvariable = self.f, font="Raleway 18", width = 18)
		self.PacketIDEntry.grid(row = 6, column = 1)
		
		self.TTLtitle = Label(self.main, text="Time to live:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.TTLtitle.grid(row=7, column=0, sticky=W)
		
		self.g= StringVar()
		self.TTLEntry = ttk.Entry(self.main, textvariable = self.g, font="Raleway 18", width = 18)
		self.TTLEntry.grid(row = 7, column = 1)
		
		self.NoPacketstitle = Label(self.main, text="Number of packets:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.NoPacketstitle.grid(row=8, column=0, sticky=W)
		
		self.h= StringVar()
		self.NoPacketEntry = ttk.Entry(self.main, textvariable = self.h, font="Raleway 18", width = 18)
		self.NoPacketEntry.grid(row = 8, column = 1)
		
		self.Flagstitle = Label(self.main, text="Flags:", fg="#63CCCA", bg="#12263A", font="Raleway 18", pady="5", padx = "20")
		self.Flagstitle.grid(row=9, column=0, sticky=W)
		
		self.flagchosen = ttk.Combobox(self.main, font="Raleway 18", width = 17)
		self.flagchosen['values'] = ('SYN', 'SYN ACK', 'ACK', 'FIN', 'FIN ACK')
		self.flagchosen.grid(row = 9, column = 1)		
		self.flagchosen.current()
		
		self.sendbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
		self.sendbuttonbg.grid(row = 0, column = 2, sticky = W)
		
		self.sendbutton = ttk.Button(self.sendbuttonbg, text = "Send", width = 6, command = self.send_btn_pressed)
		self.sendbutton.grid(row = 0, column = 0)
		
		self.packetoutputbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
		self.packetoutputbg.grid(row = 1, column = 2, rowspan = 9)
		
		self.packetoutput = Text(self.packetoutputbg, bg="#12263A", fg='#63CCCA', width = 33, height = 15, borderwidth = 1, relief = SUNKEN, font="Raleway 14")
		self.packetoutput.grid(row = 0, column = 0)
		self.packetoutput.config(state = DISABLED)
		
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
		self.valid_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
		self.valid_dec = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		sys.stdout = TextRedirector(self.packetoutput,"stdout") # takes any stdout or stderr and redirects it to the GUI
		sys.stdout = TextRedirector(self.packetoutput,"stderr")
		self.pack()
	
	def checkMac(self,mac): # Checks for valid mac address entered
		if len(mac) == 17:
			for x in range(0, len(mac)-1):
				if x == 2 or x == 5 or x == 8 or x == 11 or x == 14:
					if mac[x] != ':':
						return 0
				else:
					if mac[x].lower() not in self.valid_hex:
						return 0
			return 1
		else:
			return 0

	def checkIP(self,ip): # checks for valid ip address entered.
		if ip == '':
			return 0
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
			#print(ip[0] + "." + ip[1] + "." +  ip[2] + "." + ip[3])
			return ip[0] + "." + ip[1] + "." +  ip[2] + "." + ip[3]
		else:
			return 0

	def checkPort(self,port): # checks for valid port entered within a range.
		if port == '':
			return 0
		for x in port:
			if x not in self.valid_dec:
				return 0
			if port[0] == "0":
				port = port[1:]
		if int(port) >= 1 and int(port) < 65536:
			return port
		else:
			return 0

	def checkID(self,id): # checks for a valid ID entered for packet id.
		if id == '':
			return 0
		for x in id:
			if x not in self.valid_dec:
				return 0
			if id[0] == "0":
				id = id[1:]
		if int(id) >= 1000 and int(id) < 10000:
			return id
		else:
			return 0

	def checkTime(self,time): # checks for a valid time entered for TTL.
		if time == '':
			return 0
		for x in time:
			if x not in self.valid_dec:
				return 0
			if time[0] == "0":
				time = time[1:]
		if int(time) >= 10 and int(time) < 100:
			return time
		else:
			return 0

	def checkCount(self,count): # checks for a valid count entered for num packets.
		if count == '':
			return 0
		for x in count:
			if x not in self.valid_dec:
				return 0
			if count[0] == "0":
				count = count[1:]
		if int(count) >= 0 and int(count) < 1001:
			return count
		else:
			return 0

	
		
	def back_btn_pressed(self): # basic functionality of back button
		root.destroy()
		import MainMenu
		
	def send_btn_pressed(self):
		Type = self.typechosen.get() # gets the values entered in text boxes into variables.
		SMac = self.SMacEntry.get()
		SIP = self.SIPEntry.get()
		DIP =self.DIPEntry.get()
		SPort = self.SPortEntry.get()
		DPort = self.DPortEntry.get()
		PacketID = self.PacketIDEntry.get()
		TTL = self.TTLEntry.get()
		NumPacket = self.NoPacketEntry.get()
		Flag = self.flagchosen.get()
		if Type not in ["TCP","tcp","UDP","udp","ICMP","icmp"]: # If elif else statement to check validation of each field entered in or left blank.
			messagebox.showerror(title="ERROR!!!", message="The type " + str(Type) + " is not Valid!") # provides error message box
		elif self.checkMac(SMac) == 0 and SMac != '':
			messagebox.showerror(title="ERROR!!!", message="The sender MAC address " + str(SMac) + " is not Valid!")			
		elif self.checkIP(SIP) == 0 and SIP != '':
			messagebox.showerror(title="ERROR!!!", message="The source IP address " + str(SIP) + " is not Valid!")		
		elif self.checkIP(DIP) == 0:
			messagebox.showerror(title="ERROR!!!", message="The destination IP address " + str(DIP) + " is not Valid!")
		elif self.checkPort(SPort) == 0 and SPort != '':
			messagebox.showerror(title="ERROR!!!", message="The source port " + str(SPort) + " is not Valid!")
		elif self.checkPort(DPort) == 0 and DPort != '':
			messagebox.showerror(title="ERROR!!!", message="The destination port " + str(DPort) + " is not Valid!")
		elif Flag not in ["SYN","syn","SYN ACK","syn ack","ACK","ack","FIN","fin","FIN ACK","fin ack"]:
			messagebox.showerror(title="ERROR!!!", message="The flag " + str(Flag) + " is not Valid!")
		elif self.checkID(PacketID) == 0 and PacketID != '':
			messagebox.showerror(title="ERROR!!!", message="The packet ID " + str(PacketID) + " is not Valid!")
		elif self.checkTime(TTL) == 0 and TTL != '':
			messagebox.showerror(title="ERROR!!!", message="The TTL " + str(TTL) + " is not Valid!")
		elif self.checkCount(NumPacket) == 0 and NumPacket != '':
			messagebox.showerror(title="ERROR!!!", message="The number of packets " + str(NumPacket) + " is not Valid!")
		else:
			messagebox.showinfo(title="SUCCESS!!!", message="Exploit is Now Being Conducted!") # if all good then success text box shown
			type_insert = Type.upper()
			if SMac == '':
				mac_insert = ''
			else:
				mac_insert = "Ether(src=\"" + SMac + "\")/" # crafting of the payload for scapy to work
			if SIP == '':
				source_ip_insert = ''
			else:
				source_ip_insert = "src=\"" + SIP + '"'
			destination_ip_insert = "dst=\"" + DIP + '"'
			if SPort == '':
				source_port_insert = ''
			else:
				source_port_insert = "sport=" + str(SPort)
			if DPort == '':
				destination_port_insert = ''
			else:
				destination_port_insert = "dport=" + str(DPort)
			flagfield = ''
			if Flag in ["SYN","syn"]:
				flagfield = "S"
			elif Flag in ["SYN ACK","syn ack"]:
				flagfield = "SA"
			elif Flag in ["ACK","ack"]:
				flagfield = "A"
			elif Flag in ["FIN","fin"]:
				flagfield = "F"
			elif Flag in ["FIN ACK","fin ack"]:
				flagfield = "FA"
			flag_insert = "flags='" + flagfield + "'"
			if PacketID == '':
				packet_id_insert = ''
			else:
				packet_id_insert = "id=" + str(PacketID)
			if TTL == '':
				time_insert = ''
			else:
				time_insert = "ttl=" + str(TTL)
			if NumPacket == '':
				count_insert = ''
			else:
				count_insert = "count=" + str(NumPacket)

			packet = mac_insert + "IP(" + source_ip_insert

			if destination_ip_insert != '':
				if source_ip_insert != '':
					packet += ", "
				packet += destination_ip_insert

			if packet_id_insert != '':
				packet += ", " + packet_id_insert

			if time_insert != '':
				packet += ", " + time_insert
				
			packet += ")/" + type_insert + '('

			if Type.lower() == "tcp" or Type.lower() == "udp":
				packet += source_port_insert

				if destination_port_insert != '':
					packet += ", " + destination_port_insert

				if Type.lower() == "tcp":
					if flag_insert != '':
						packet += ", " + flag_insert

			packet += ')'

			if count_insert != '':
				packet += ", " + count_insert
			#print(count_insert)
			print(packet)

			if mac_insert != '':
				send(packet) # when the packet is crafted, send the packet using scapy python module.
				#os.system('python -m scapy')
				#os.system("send(" + packet + ")")
			else:
				#os.system('python -m scapy')
				#os.system("send(" + packet + ")")
				send(packet)
			
		#print(Type)
		#print(SMac)
		#print(SIP)
		#print(DIP)
		#print(SPort)
		#print(DPort)
		#print(PacketID)
		#print(TTL)
		#print(NumPacket)
		#print(Flag)
		#messagebox.showinfo(title="SUCCESS!!!", message="Exploit is Now Being Conducted!")
		
		
		
		
		
		
	
	
	

root = Tk()
root.option_add("*TCombobox*Listbox*Background", '#12263A')
root.option_add("*TCombobox*Listbox*Foreground", '#63CCCA')
root.option_add("*TCombobox*Listbox*Font", 'Raleway 17')

wmgstyle = ttk.Style()
wmgstyle.theme_create('wmgstyle', parent = 'alt', settings = {'TCombobox': {'configure': {'fieldbackground': '#63CCCA', 'background': '#12263A', 'foreground': '#12263A', 'arrowcolor': "#63CCCA" , 'arrowsize' : '20', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TEntry': {'configure': {'fieldbackground': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TButton': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA", 'font': "Raleway 17"}}})

wmgstyle.theme_use("wmgstyle")  # Tkinter settings set for window

lf = BaseFrame(root)
root.geometry("1024x600")
root.title("Frame Template")
root.resizable(False, False)
root.mainloop()

