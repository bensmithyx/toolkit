from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tm
from PIL import ImageTk, Image
import os

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
    	
    	self.NWAbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="5", padx = "10")
    	self.NWAbuttonbg.grid(row = 0, column = 1, sticky = W+E)
    	
    	self.NWAbutton = ttk.Button(self.NWAbuttonbg, text = "Network Attacks", width = 13, command = self.nwa_btn_pressed)
    	self.NWAbutton.grid(row = 0, column = 0)
    	
    	self.PMbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
    	self.PMbuttonbg.grid(row = 0, column = 2, sticky = W+E)
    	
    	self.PMbutton = ttk.Button(self.PMbuttonbg, text = "Packet Masquerading", width = 17, command = self.pm_btn_pressed)
    	self.PMbutton.grid(row = 0, column = 0)
    	
    	self.Scanbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
    	self.Scanbuttonbg.grid(row = 0, column = 3, sticky = W+E)
    	
    	self.Scanbutton = ttk.Button(self.Scanbuttonbg, text = "Scanner", width = 11, command = self.scanner_btn_pressed)
    	self.Scanbutton.grid(row = 0, column = 0)
    	
    	self.Chatbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
    	self.Chatbuttonbg.grid(row = 0, column = 4, sticky = W+E)
    	
    	self.Chatbutton = ttk.Button(self.Chatbuttonbg, text = "Chatroom", width = 10, command = self.chatroom_btn_pressed)
    	self.Chatbutton.grid(row = 0, column = 0)
    	
    	self.Reversebuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
    	self.Reversebuttonbg.grid(row = 1, column = 1, sticky = W+E)
    	
    	self.Reversebutton = ttk.Button(self.Reversebuttonbg, text = "ReverseShell", width = 13, command = self.reverse_btn_pressed)
    	self.Reversebutton.grid(row = 0, column = 0)
    	
    	self.Enumbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
    	self.Enumbuttonbg.grid(row = 1, column = 2, sticky = W+E)
    	
    	self.Enumbutton = ttk.Button(self.Enumbuttonbg, text = "Enumerator", width = 17, command = self.enumerator_btn_pressed)
    	self.Enumbutton.grid(row = 0, column = 0)
    	
    	self.Pullbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="0", padx = "10")
    	self.Pullbuttonbg.grid(row = 1, column = 3, sticky = W+E)
    	
    	self.Pullbutton = ttk.Button(self.Pullbuttonbg, text = "PullExploits", width = 11, command = self.pull_btn_pressed)
    	self.Pullbutton.grid(row = 0, column = 0)
    	self.termf = Frame(self.main, height=350, width=1010)
    	self.termf.grid(row=2, column=0, columnspan=5)
    	wid = self.termf.winfo_id()
    	#os.system('xterm -into %d -geometry 165x27 -sb & ' % wid)
    	os.system('xterm -into %d -geometry 165x27 -sb & ' % wid)
    	
    	self.terms = Label(self.footer, text="The company do not take responsibility for any misue of this product.", fg="#63CCCA", bg="#12263A", font="Raleway 16", pady="10")
    	self.terms.grid(row=0, column=1, sticky=N)
    	
    	self.header.configure(background='#12263A')
    	self.titlelogo.configure(background='#12263A')
    	self.main.configure(background='#12263A')
    	self.footer.configure(background='#12263A')
    	
    	self.pack()
    
    def nwa_btn_pressed(self):
    	root.destroy()
    	import NWA
    	
    def pm_btn_pressed(self):
    	root.destroy()
    	import PacketMasq

    def scanner_btn_pressed(self):
    	root.destroy()
    	import Scanner

    def chatroom_btn_pressed(self):
    	import Chatroom

    def reverse_btn_pressed(self):
    	root.destroy()
    	import Reverse

    def enumerator_btn_pressed(self):
    	root.destroy()
    	import Enumerator

    def pull_btn_pressed(self):
    	root.destroy()
    	import PullExploits

root = Tk()
root.option_add("*TCombobox*Listbox*Background", '#12263A')
root.option_add("*TCombobox*Listbox*Foreground", '#63CCCA')
root.option_add("*TCombobox*Listbox*Font", 'Raleway 21')

wmgstyle = ttk.Style()
wmgstyle.theme_create('wmgstyle', parent = 'alt', settings = {'TCombobox': {'configure': {'fieldbackground': '#63CCCA', 'background': '#12263A', 'foreground': '#12263A', 'arrowcolor': "#63CCCA" , 'arrowsize' : '20', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TEntry': {'configure': {'fieldbackground': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TButton': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA", 'font': "Raleway 21"}}})

wmgstyle.theme_use("wmgstyle")
lf = BaseFrame(root)
root.geometry("1024x600")
root.title("CTF Toolkit")
root.iconphoto(False, PhotoImage(file="Icon.png"))
root.resizable(False, False)
root.mainloop()

