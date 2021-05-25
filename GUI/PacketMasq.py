from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tm
from PIL import ImageTk, Image

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
    	
    	self.pack()
    	
    	
    def back_btn_pressed(self):
    	root.destroy()
    	import MainMenu
    	
    def send_btn_pressed(self):
    	Type = self.typechosen.get()
    	SMac = self.SMacEntry.get()
    	SIP = self.SIPEntry.get()
    	DIP =self.DIPEntry.get()
    	SPort = self.SPortEntry.get()
    	DPort = self.DPortEntry.get()
    	PacketID = self.PacketIDEntry.get()
    	TTL = self.TTLEntry.get()
    	NumPacket = self.NoPacketEntry.get()
    	Flag = self.flagchosen.get()
    	print(Type)
    	print(SMac)
    	print(SIP)
    	print(DIP)
    	print(SPort)
    	print(DPort)
    	print(PacketID)
    	print(TTL)
    	print(NumPacket)
    	print(Flag)
    	
    	
    	
    	
    	
    
    
    

root = Tk()
root.option_add("*TCombobox*Listbox*Background", '#12263A')
root.option_add("*TCombobox*Listbox*Foreground", '#63CCCA')
root.option_add("*TCombobox*Listbox*Font", 'Raleway 17')

wmgstyle = ttk.Style()
wmgstyle.theme_create('wmgstyle', parent = 'alt', settings = {'TCombobox': {'configure': {'fieldbackground': '#63CCCA', 'background': '#12263A', 'foreground': '#12263A', 'arrowcolor': "#63CCCA" , 'arrowsize' : '20', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TEntry': {'configure': {'fieldbackground': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TButton': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA", 'font': "Raleway 17"}}})

wmgstyle.theme_use("wmgstyle")

lf = BaseFrame(root)
root.geometry("1024x600")
root.title("Frame Template")
root.resizable(False, False)
root.mainloop()

