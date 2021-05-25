# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from playsound import playsound
import socket, threading, datetime, time, sys, os, subprocess, math, random, gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

class BaseFrame(Frame):
    def __init__(self, master):
    	super().__init__(master)
    	
    	self.header = Frame(self, width = 325, height = 50)
    	self.main = Frame(self, width = 325, height = 550)
    	
    	self.header.grid(row=0, column=0, sticky=N+E)
    	self.header.grid_propagate(False)
    	self.main.grid(row=1, column=0, sticky=N+E)
    	self.main.grid_propagate(False)
    	
    	self.titlelogo = Canvas(self.header, width = 50, height = 50, highlightthickness = 0)
    	self.titlelogo.grid(row=0, column=0, sticky=W)
    	
    	self.img = Image.open("Logo.png")
    	self.img = self.img.resize((50, 50), Image.ANTIALIAS)
    	self.img1 = ImageTk.PhotoImage(self.img)
    	self.titlelogo.create_image(0.5,1,anchor = N+W, image = self.img1)
    	
    	self.title = Label(self.header, text="CTF Chatroom", fg="#63CCCA", bg="#12263A", font="Raleway 24 bold", pady="10", padx = "10")
    	self.title.grid(row=0, column=1, sticky=N+W)
    	
    	self.usernametitle = Label(self.main, text="Username:", fg="#63CCCA", bg="#12263A", font="Raleway 14", pady="5", padx = "5")
    	
    	self.usernametitle.grid(row = 0, column = 0, sticky=S+W)
    	
    	self.usernameentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="5", padx = "5")
    	self.connectbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="5", padx = "5")
    	
    	self.usernameentrybg.grid(row = 1, column = 0, sticky=W)
    	self.connectbuttonbg.grid(row = 1, column = 1, columnspan = 2, sticky=W)
    
    	self.v = StringVar()
    	self.usernameentry = ttk.Entry(self.usernameentrybg, textvariable = self.v, font="Raleway 14", width = 18)
    	self.usernameentry.grid(row = 0, column = 0)
    	self.usernameentry.bind("<Return>", (lambda event: self.connect_btn_pressed()))
    	
    	self.connectbutton = ttk.Button(self.connectbuttonbg, text = "Connect", width = 7, command = self.connect_btn_pressed)
    	self.connectbutton.grid(row = 0, column = 0)

    	self.messageoutput = Text(self.main, bg="#12263A", fg='#63CCCA', width = 34, height = 23, borderwidth = 1, relief = SUNKEN, font="Raleway 10", padx = "10")
    	self.messageoutput.grid(row = 2, column = 0, sticky = "e", columnspan = 2)
    	self.messageoutput.config(state = DISABLED)

    	self.messageoutput.tag_config("tag_username", foreground="#F40D01")
    	self.messageoutput.tag_config("tag_command", foreground="darkgreen")
    	self.messageoutput.tag_config("tag_your_message", foreground="#F3FFC6")

    	
    	self.outscroll = ttk.Scrollbar(self.main, command=self.messageoutput.yview)
    	self.outscroll.grid(row=2, column=2, sticky='nse')
    	self.messageoutput['yscrollcommand'] = self.outscroll.set

    	self.textpadding = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, height = 5)
    	self.textpadding.grid(row = 3, column = 0, columnspan = 3)
    	
    	self.messageinput = Text(self.main, bg="#63CCCA", fg='#12263A', pady = "10", width = 36, height = 2, borderwidth = 1, relief = SUNKEN, font="Raleway 10")
    	self.messageinput.grid(row = 4, column = 0, columnspan = 2)
    	self.messageinput.bind("<Return>", (lambda event: self.getChatMessage(self.messageinput.get("1.0", END))))
    	self.messageinput.config(state = DISABLED)

    	self.inscroll = ttk.Scrollbar(self.main, command=self.messageinput.yview)
    	self.inscroll.grid(row=4, column=2, sticky='nse')
    	self.messageinput['yscrollcommand'] = self.inscroll.set

    	self.header.configure(background='#12263A')
    	self.titlelogo.configure(background='#12263A')
    	self.main.configure(background= '#12263A')
    	
    	self.pack()

    padding = 30

    alphabet = [' ', '!', 'w', 's', 'o', 'k', 'g', 'c', '.', 'z', 'v', 'r', 'n', 'j', 'f', 'b', ',', 'y', 'u', 'q', 'm', 'i', 'e', 'a', '?', 'x', 't', 'p', 'l', 'h', 'd', '>', '}', ')', '^', '£', '+', '\\', ';', '7', '3', 'Y', 'U', 'Q', 'M', 'I', 'E', 'A', '<', '{', '(', '%', '@', '-', '"', '0', '6', '2', 'X', 'T', 'P', 'L', 'H', 'D', '~', ']', '*', '$', '_', '/', "'", '9', '5', '1', 'W', 'S', 'O', 'K', 'G', 'C', '`', '[', '&', '#', '=', '|', ':', '8', '4', 'Z', 'V', 'R', 'N', 'J', 'F', 'B']

    latency_messages = ["Thirteen", "Thursday", "Princess", "Assonant", "Thousand", "Fourteen", "Language", "Chipotle", "American", "Business", "Favorite", "Elephant", "Children", "Birthday", "Mountain", "Feminine", "Football", "Kindness", "Syllable", "Abdicate", "Treasure", "Virginia", "Envelope", "Strength", "Together", "Memories", "Darkness", "February", "Sandwich", "Calendar", "Bullying", "Equation", "Violence", "Marriage", "Building", "Internal", "Function", "November", "Drooping", "Abortion", "Victoria", "Squirrel", "Tomorrow", "Champion", "self.sound_sentence", "Personal", "Remember", "Daughter", "Hospital", "Ordinary"]

    username = " "
    userid = 'i'
    passcount = 0
    users = ['', '', '', '', '', '', '', '', '', '']
    muted = [False, False, False, False, False, False, False, False, False, False]
    kicked = False
    reloaded = False
    recieving = False
    admin = False
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sent = str(dir_path) + "/Message_Sent.mp3"
    recieved = str(dir_path) + "/Message_Recieved.mp3"
    icon = str(dir_path) + "/icon.png"
    
    def sound_recieved(self):
    	playsound(self.recieved)
    
    def sound_sent(self):
    	playsound(self.sent)
    
    client = None
    HOST_ADDR = "ping.cyb3r.lol"
    HOST_ADDR = "172.67.137.126"
    HOST_PORT = 2521

    def connect_btn_pressed(self):
        if len(self.usernameentry.get()) < 1:
            messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
        else:
            self.username = self.usernameentry.get()
            self.connect_to_server(self.username)

    def decode_binary(self, data):
        nums = []
        out = []
        count = 0
        temp = ""
        for b in data:
            if count == 0:
                count += 1
                pass
            else:
                if int(b) >= self.padding:
                    temp += "1"
                else:
                    temp += "0"
                count += 1
                if count == 9:
                    nums.append(int(temp))
                    temp = ""
                    count = 0
        for n in nums:
            num = 256 - int(str(n), 2)
            if num == 128:
                num = 0
            if num < 96:
                out.append(num)
        return out

    def encode_binary(self, value):
        if value == 0:
            num = "18000000"
        else:
            bits = 128 - value
            num = '{0:b}'.format(bits)
            while len(num) < 7:
                num = "0%s" % num
            num = "11%s" % num
        return num

    def check(self, out, new, x):
        if out[new] == '':
            out[new] = x
            return out
        else:
            self.check(out, new+1, x)

    def shift(self):
        x = datetime.datetime.now()
        year = x.year
        month = x.month
        day = x.day
        intshift = ((day**2) + month) * year
        out = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
        for x in range(0, len(self.alphabet)):
            z = len(self.alphabet) - x
            new = intshift % z
            self.check(out, new, self.alphabet[x])
        return out

    def encode_data(self, data):
        global setting
        outputlist = []
        for d in data:
            newloc = self.alphabet.index(d)
            outputlist.append(setting[newloc])
        output = "".join(outputlist)
        return output

    def decode_data(self, data):
        global setting
        outputlist = []
        for d in data:
            outputlist.append(setting[d])
        output = "".join(outputlist)
        return output

    def send_data(self, data, prefix):
        global client, setting
        client.send(prefix.encode())
        client.send(str(self.userid).encode())
        for d in data:
            for s in self.encode_binary(setting.index(str(d))):
                client.send(str(self.userid).encode())
                time.sleep(((float(s) * 80) + 1) / 2000)
        client.send(str(self.userid).encode())
        client.send("f".encode())

    def round_down(self, n, decimals=0):
        multiplier = 10 ** decimals
        rounded = math.floor(n * multiplier) / multiplier
        return rounded

    def get_latency(self):
        global client
        latency_data = []
        actual_shift = []
        possible_shift = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        score = 0
        max_shift = 0
        latency_shift = 0
        latency_word1 = random.choice(self.latency_messages)
        while True:
            latency_word2 = random.choice(self.latency_messages)
            if latency_word2 != latency_word1:
                break
        while True:
            latency_word3 = random.choice(self.latency_messages)
            if latency_word3 != latency_word1 or latency_word3 != latency_word2:
                break
        latency_words = latency_word1 + latency_word2 + latency_word3
        self.send_data(latency_words, "p")
        while True:
            t1 = time.time()
            server_data  = client.recv(1)
            t0 = time.time()
            data = int(self.round_down(t0-t1,2) * 2000)
            latency_data.append(data)
            server_data = server_data.decode("utf-8")
            if str(server_data) == "f":
                del latency_data[0:3]
                break
        
        for x in range(0, 200):
            score = 0
            self.padding = x
            latency_test = self.decode_data(self.decode_binary(latency_data))
            for y in range(0, len(latency_test)):
                if latency_words[y] == latency_test[y]:
                    score += 5
            if score >= 90:
                possible_shift[x] = score

        for p in range(0, len(possible_shift)-1):
            if possible_shift[p] > max_shift:
                max_shift = possible_shift[p]

        if max_shift != 0:
            for q in range(0, len(possible_shift)-1):
                if possible_shift[q] == max_shift:
                    actual_shift.append(q)
            if len(actual_shift) > 1:
                latency_shift = actual_shift[int((len(actual_shift)-1)/2)]
                return latency_shift
            elif len(actual_shift) == 1:
                latency_shift = actual_shift[0]
                return latency_shift
            else:
                return "NULL"
        else:
            return "NULL"

    def send_notification(self, username, message):
        Notify.init("Chatroom")
        notification = Notify.Notification.new(self.username, message, self.icon)
        notification.set_urgency(0)
        notification.show()


    def connect_to_server(self, name):
        global client, setting
        setting = self.shift()
        self.shift_count = 0
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.HOST_ADDR, self.HOST_PORT))
            client.send("x".encode())
            while True:
                syn_ack = client.recv(1)
                syn_ack = syn_ack.decode("utf-8")
                if str(syn_ack) == "y":
                    threading._start_new_thread(self.send_data, (name, "s"))
                    break
            id_data = []
            while True:
                server_userid = client.recv(1)
                server_userid = server_userid.decode("utf-8")
                if str(server_userid) == "n":
                    server_userid = client.recv(1)
                    self.userid = server_userid.decode("utf-8")
                    server_fin = client.recv(1)
                    break
            while True:
                test_latency = self.get_latency()
                if test_latency != "NULL":
                    self.padding = test_latency
                    client.send("q".encode())
                    break
                else:
                    if self.shift_count < 4:
                        self.shift_count += 1
                    else:
                        client.send("q".encode())
                        #raise Exception("Sorry, no latency shift could be found")
                        self.padding = 30
                        break

            if self.userid != "i":
                texts = self.messageoutput.get("1.0", END).strip()
                self.messageoutput.config(state=NORMAL)
                if len(texts) < 1:
                    self.messageoutput.insert(END, "Welcome ")
                    self.messageoutput.insert(END, self.username, "tag_your_message")
                    self.messageoutput.insert(END, ". Please type '")
                    self.messageoutput.insert(END, "/help", "tag_command")
                    self.messageoutput.insert(END, "' to list all commands.")
                else:
                    self.messageoutput.insert(END, "\n\nWelcome ")
                    self.messageoutput.insert(END, self.username, "tag_your_message")
                    self.messageoutput.insert(END, ". Please type '")
                    self.messageoutput.insert(END, "/help", "tag_command")
                    self.messageoutput.insert(END, "' to list all commands.")

                self.messageoutput.config(state=DISABLED)
                self.messageoutput.see(END)

            self.usernameentry.config(state=DISABLED)
            self.connectbutton.config(state=DISABLED)
            self.messageinput.config(state=NORMAL)

            threading._start_new_thread(self.receive_message_from_server, (client, "m"))
        except Exception as e:
            messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + self.HOST_ADDR + " on port: " + str(self.HOST_PORT) + " Server may be Unavailable. Try again later")

    def receive_message_from_server(self, sck, m):
        while True:
            try:
                from_server = sck.recv(1)
                from_server = from_server.decode("utf-8")
                self.recieving = True
                message_data = []
                user_data = []
                leave_data = []
                change_data = []
                while True:
                    if str(from_server) == "w":
                        break
                    if str(from_server) == "f":
                        self.recieving = False
                        break
                    t1 = time.time()
                    server_data  = sck.recv(1)
                    t0 = time.time()
                    data = int(self.round_down(t0-t1,2) * 2000)
                    if str(from_server) == "u":
                        server_data = server_data.decode("utf-8")
                        if str(server_data) == "f":
                            self.recieving = False
                            del user_data[0:2]
                            user_name = self.decode_data(self.decode_binary(user_data))
                            self.users[int(id_data)] = str(user_name)
                            texts = self.messageoutput.get("1.0", END).strip()
                            self.messageoutput.config(state=NORMAL)
                            if len(texts) < 1:
                                self.messageoutput.insert(END + str(user_name), "tag_username")
                                self.messageoutput.insert(END, " has joined the chat.")
                            else:
                                self.messageoutput.insert(END, "\n\n" + str(user_name), "tag_username")
                                self.messageoutput.insert(END, " has joined the chat.")
                            self.messageoutput.config(state=DISABLED)
                            self.messageoutput.see(END)
                            user_data = []
                            break
                        
                        user_data.append(data)
                        id_data = server_data
                        
                    if str(from_server) == "l":
                        server_data = server_data.decode("utf-8")
                        if str(server_data) == "f":
                            self.recieving = False
                            texts = self.messageoutput.get("1.0", END).strip()
                            self.messageoutput.config(state=NORMAL)
                            if len(texts) < 1:
                                self.messageoutput.insert(END + str(self.users[int(leave_data[0])]), "tag_username")
                                self.messageoutput.insert(END, " has left the chat.")
                            else:
                                self.messageoutput.insert(END, "\n\n" + str(self.users[int(leave_data[0])]), "tag_username")
                                self.messageoutput.insert(END, " has left the chat.")
                            self.messageoutput.config(state=DISABLED)
                            self.messageoutput.see(END)
                            leave_data = []
                            break
                        leave_data.append(str(server_data))

                    if str(from_server) == "b":
                        server_data = server_data.decode("utf-8")
                        if str(server_data) == "f":
                            self.recieving = False
                            if str(self.userid) == str(kicked_idx):
                                client.send("a".encode())
                            break

                        kicked_idx = str(server_data)

                    if str(from_server) == "k":
                        server_data = server_data.decode("utf-8")
                        if str(server_data) == "f":
                            self.recieving = False
                            texts = self.messageoutput.get("1.0", END).strip()
                            self.messageoutput.config(state=NORMAL)
                            if int(leave_data[0]) == int(self.userid):
                                if len(texts) < 1:
                                    self.messageoutput.insert(END, "You", "tag_your_message")
                                    self.messageoutput.insert(END, " have been ")
                                    self.messageoutput.insert(END, "kicked", "tag_command")
                                    self.messageoutput.insert(END, " from the chat.")
                                else:
                                    self.messageoutput.insert(END, "\n\nYou", "tag_your_message")
                                    self.messageoutput.insert(END, " have been ")
                                    self.messageoutput.insert(END, "kicked", "tag_command")
                                    self.messageoutput.insert(END, " from the chat.")
                                self.kicked = True
                                
                            else:
                                if len(texts) < 1:
                                    self.messageoutput.insert(END + str(self.users[int(leave_data[0])]), "tag_username")
                                    self.messageoutput.insert(END, " has been ")
                                    self.messageoutput.insert(END, "kicked", "tag_command")
                                    self.messageoutput.insert(END, " from the chat.")
                                else:
                                    self.messageoutput.insert(END, "\n\n" + str(self.users[int(leave_data[0])]), "tag_username")
                                    self.messageoutput.insert(END, " has been ")
                                    self.messageoutput.insert(END, "kicked", "tag_command")
                                    self.messageoutput.insert(END, " from the chat.")
                            self.messageoutput.config(state=DISABLED)
                            self.messageoutput.see(END)
                            leave_data = []
                            break
                        leave_data.append(str(server_data))

                    if str(from_server) == "c":
                        server_data = server_data.decode("utf-8")
                        if str(server_data) == "f":
                            self.recieving = False
                            if int(self.userid) == int(change_data[0]):
                                self.userid = int(change_data[1])
                                change_data = []
                                break
                            else:
                                self.users[int(change_data[1])] = self.users[int(change_data[0])]
                                self.users[int(change_data[0])] = ''
                                change_data = []
                                break
                        change_data.append(str(server_data))

                    if str(from_server) == "s":
                        server_data = server_data.decode("utf-8")
                        if str(server_data) == "f":
                            self.recieving = False
                            del message_data[0:2]
                            server_message = self.decode_data(self.decode_binary(message_data))
                            if self.muted[int(id_data)] == False:
                                texts = self.messageoutput.get("1.0", END).strip()
                                self.messageoutput.config(state=NORMAL)
                                if len(texts) < 1:
                                    self.messageoutput.insert(END + str(self.users[int(id_data)]) + " >> ", "tag_username")
                                    self.messageoutput.insert(END, server_message)
                                else:
                                    self.messageoutput.insert(END, "\n\n"+ str(self.users[int(id_data)]) + " >> ", "tag_username")
                                    self.messageoutput.insert(END, server_message)

                                self.messageoutput.config(state=DISABLED)
                                self.messageoutput.see(END)
                                self.send_notification(str(self.users[int(id_data)]), str(server_message))
                                dir_path = os.path.dirname(os.path.realpath(__file__))
                                self.sound_recieved()
                            message_data = []
                            break
                        message_data.append(data)
                        id_data = server_data
                if self.kicked == True:
                    break
            except:
                pass
            
        client.close()
        self.messageinput.config(state=DISABLED)

    def getChatMessage(self, msg):
        threading._start_new_thread(self.startChatMessage, (msg, "y"))


    def startChatMessage(self, msg, y):
        msg = msg.replace('\n', '')
        self.messageoutput.see(END)
        self.messageinput.delete('1.0', END)
        test_msg = msg

        if test_msg != "":
            if test_msg[0] == "/":
                test_msg = test_msg[1:]
                if test_msg.lower() == "help":
                    texts = self.messageoutput.get("1.0", END).strip()
                    self.messageoutput.config(state=NORMAL)
                    if len(texts) < 1:
                        self.messageoutput.insert(END, "Help:\n\n", "tag_your_message")
                        self.messageoutput.insert(END, "/help ", "tag_command")
                        self.messageoutput.insert(END, "- Lists all the commands.\n\n")
                        self.messageoutput.insert(END, "/admin {password} ", "tag_command")
                        self.messageoutput.insert(END, "- Sign in as an self.admin.\n\n")
                        self.messageoutput.insert(END, "/kick {username} ", "tag_command")
                        self.messageoutput.insert(END, "- Kick a user from the chat.\n\n")
                        self.messageoutput.insert(END, "/mute {username} ", "tag_command")
                        self.messageoutput.insert(END, "- Mute a user on your chat.\n\n")
                        self.messageoutput.insert(END, "/unmute {username} ", "tag_command")
                        self.messageoutput.insert(END, "- Un-mute a user on your chat.\n\n")
                        self.messageoutput.insert(END, "/reload ", "tag_command")
                        self.messageoutput.insert(END, "- Reload all saved self.usernames in your chat.\n\n")
                        self.messageoutput.insert(END, "/exit ", "tag_command")
                        self.messageoutput.insert(END, "- Quit the chat.")
                    else:
                        self.messageoutput.insert(END, "\n\nHelp:\n\n", "tag_your_message")
                        self.messageoutput.insert(END, "/help ", "tag_command")
                        self.messageoutput.insert(END, "- Lists all the commands.\n\n")
                        self.messageoutput.insert(END, "/admin {password} ", "tag_command")
                        self.messageoutput.insert(END, "- Sign in as an self.admin.\n\n")
                        self.messageoutput.insert(END, "/kick {username} ", "tag_command")
                        self.messageoutput.insert(END, "- Kick a user from the chat.\n\n")
                        self.messageoutput.insert(END, "/mute {username} ", "tag_command")
                        self.messageoutput.insert(END, "- Mute a user on your chat.\n\n")
                        self.messageoutput.insert(END, "/unmute {username} ", "tag_command")
                        self.messageoutput.insert(END, "- Un-mute a user on your chat.\n\n")
                        self.messageoutput.insert(END, "/reload ", "tag_command")
                        self.messageoutput.insert(END, "- Reload all saved self.usernames in your chat.\n\n")
                        self.messageoutput.insert(END, "/exit ", "tag_command")
                        self.messageoutput.insert(END, "- Quit the chat.")
                    self.messageoutput.config(state=DISABLED)
                
                elif test_msg.lower() == "exit":
                    client.close()
                    root.destroy()
                    sys.exit()

                elif str(test_msg[0:5].lower()) == "admin":
                    password = test_msg[6:]
                    hidden = "*" * int(len(password))
                    texts = self.messageoutput.get("1.0", END).strip()
                    self.messageoutput.config(state=NORMAL)
                    if len(texts) < 1:
                        self.messageoutput.insert(END, "You >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/admin ", "tag_command")
                        self.messageoutput.insert(END, hidden)
                    else:
                        self.messageoutput.insert(END, "\n\nYou >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/admin ", "tag_command")
                        self.messageoutput.insert(END, hidden)
                    self.messageoutput.config(state=DISABLED)
                    if str(password) == "Pa3sw0rd" and self.passcount < 5:
                        self.admin = True
                        texts = self.messageoutput.get("1.0", END).strip()
                        self.messageoutput.config(state=NORMAL)
                        if len(texts) < 1:
                            self.messageoutput.insert(END, "You are now an ")
                            self.messageoutput.insert(END, "admin", "tag_command")
                            self.messageoutput.insert(END, ".")
                        else:
                            self.messageoutput.insert(END, "\n\nYou are now an ")
                            self.messageoutput.insert(END, "admin", "tag_command")
                            self.messageoutput.insert(END, ".")
                        self.messageoutput.config(state=DISABLED)

                    else:
                        if self.passcount >= 5:
                            texts = self.messageoutput.get("1.0", END).strip()
                            self.messageoutput.config(state=NORMAL)
                            if len(texts) < 1:
                                self.messageoutput.insert(END, "You have exceeded your ")
                                self.messageoutput.insert(END, "admin", "tag_command")
                                self.messageoutput.insert(END, " login attempts.")
                            else:
                                self.messageoutput.insert(END, "\n\nYou have exceeded your ")
                                self.messageoutput.insert(END, "admin", "tag_command")
                                self.messageoutput.insert(END, " login attempts.")
                            self.messageoutput.config(state=DISABLED)
                            
                        else:
                            self.passcount += 1
                            texts = self.messageoutput.get("1.0", END).strip()
                            self.messageoutput.config(state=NORMAL)
                            if len(texts) < 1:
                                self.messageoutput.insert(END, "Incorrect ")
                                self.messageoutput.insert(END, "admin", "tag_command")
                                self.messageoutput.insert(END, " password.")
                            else:
                                self.messageoutput.insert(END, "\n\nIncorrect ")
                                self.messageoutput.insert(END, "admin", "tag_command")
                                self.messageoutput.insert(END, " password.")
                            self.messageoutput.config(state=DISABLED)
                        

                elif test_msg.lower() == "reload":
                    texts = self.messageoutput.get("1.0", END).strip()
                    self.messageoutput.config(state=NORMAL)
                    if len(texts) < 1:
                        self.messageoutput.insert(END, "You >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/reload ", "tag_command")
                    else:
                        self.messageoutput.insert(END, "\n\nYou >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/reload ", "tag_command")
                    self.messageoutput.config(state=DISABLED)
                    while True:
                        if self.recieving == False:
                            client.send("r".encode())
                            client.send("f".encode())
                            break

                    texts = self.messageoutput.get("1.0", END).strip()
                    self.messageoutput.config(state=NORMAL)
                    if len(texts) < 1:
                        self.messageoutput.insert(END, "All usernames have been ")
                        self.messageoutput.insert(END, "reloaded", "tag_command")
                        self.messageoutput.insert(END, ".")
                    else:
                        self.messageoutput.insert(END, "\n\nAll usernames have been ")
                        self.messageoutput.insert(END, "reloaded", "tag_command")
                        self.messageoutput.insert(END, ".")
                    self.messageoutput.config(state=DISABLED)
                    self.recieving = False

                elif str(test_msg[0:4].lower()) == "kick":
                    test_msg = test_msg[5:]
                    texts = self.messageoutput.get("1.0", END).strip()
                    self.messageoutput.config(state=NORMAL)
                    if len(texts) < 1:
                        self.messageoutput.insert(END, "You >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/kick ", "tag_command")
                        self.messageoutput.insert(END, test_msg)
                    else:
                        self.messageoutput.insert(END, "\n\nYou >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/kick ", "tag_command")
                        self.messageoutput.insert(END, test_msg)

                    self.messageoutput.config(state=DISABLED)
                    try:
                        nameid = self.users.index(test_msg)
                        if self.admin == True:
                            while True:
                                if self.recieving == False:
                                    client.send("k".encode())
                                    client.send(str(nameid).encode())
                                    client.send("f".encode())
                                    break
                        else:
                            texts = self.messageoutput.get("1.0", END).strip()
                            self.messageoutput.config(state=NORMAL)
                            if len(texts) < 1:
                                self.messageoutput.insert(END, "You are not an ")
                                self.messageoutput.insert(END, "admin", "tag_command")
                                self.messageoutput.insert(END, ".")
                            else:
                                self.messageoutput.insert(END, "\n\nYou are not an ")
                                self.messageoutput.insert(END, "admin", "tag_command")
                                self.messageoutput.insert(END, ".")
                            self.messageoutput.config(state=DISABLED)
                    
                    except:
                        texts = self.messageoutput.get("1.0", END).strip()
                        self.messageoutput.config(state=NORMAL)
                        if len(texts) < 1:
                            self.messageoutput.insert(END, "User not found.")
                        else:
                            self.messageoutput.insert(END, "\n\nUser not found.")
                        self.messageoutput.config(state=DISABLED)

                elif str(test_msg[0:4].lower()) == "mute":
                    test_msg = test_msg[5:]
                    texts = self.messageoutput.get("1.0", END).strip()
                    self.messageoutput.config(state=NORMAL)
                    if len(texts) < 1:
                        self.messageoutput.insert(END, "You >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/mute ", "tag_command")
                        self.messageoutput.insert(END, test_msg)
                    else:
                        self.messageoutput.insert(END, "\n\nYou >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/mute ", "tag_command")
                        self.messageoutput.insert(END, test_msg)
                    self.messageoutput.config(state=DISABLED)
                    
                    try:
                        nameid = self.users.index(test_msg)
                        self.muted[int(nameid)] = True
                        
                        texts = self.messageoutput.get("1.0", END).strip()
                        self.messageoutput.config(state=NORMAL)
                        if len(texts) < 1:
                            self.messageoutput.insert(END + str(test_msg), "tag_username")
                            self.messageoutput.insert(END, " has been ")
                            self.messageoutput.insert(END, "muted", "tag_command")
                            self.messageoutput.insert(END, " in your chat.")
                        else:
                            self.messageoutput.insert(END, "\n\n" + str(test_msg), "tag_username")
                            self.messageoutput.insert(END, " has been ")
                            self.messageoutput.insert(END, "muted", "tag_command")
                            self.messageoutput.insert(END, " in your chat.")
                        self.messageoutput.config(state=DISABLED)
                    
                    except:
                        texts = self.messageoutput.get("1.0", END).strip()
                        self.messageoutput.config(state=NORMAL)
                        if len(texts) < 1:
                            self.messageoutput.insert(END, "User not found.")
                        else:
                            self.messageoutput.insert(END, "\n\nUser not found.")
                        self.messageoutput.config(state=DISABLED)
                        
                elif test_msg[0:6].lower() == "unmute":
                    test_msg = test_msg[7:]
                    texts = self.messageoutput.get("1.0", END).strip()
                    self.messageoutput.config(state=NORMAL)
                    if len(texts) < 1:
                        self.messageoutput.insert(END, "You >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/unmute ", "tag_command")
                        self.messageoutput.insert(END, test_msg)
                    else:
                        self.messageoutput.insert(END, "\n\nYou >> ", "tag_your_message")
                        self.messageoutput.insert(END, "/unmute ", "tag_command")
                        self.messageoutput.insert(END, test_msg)
                    self.messageoutput.config(state=DISABLED)
                    
                    try:
                        nameid = self.users.index(test_msg)
                        self.muted[int(nameid)] = False

                        texts = self.messageoutput.get("1.0", END).strip()
                        self.messageoutput.config(state=NORMAL)
                        if len(texts) < 1:
                            self.messageoutput.insert(END + str(test_msg), "tag_username")
                            self.messageoutput.insert(END, " has been ")
                            self.messageoutput.insert(END, "unmuted", "tag_command")
                            self.messageoutput.insert(END, " in your chat.")
                        else:
                            self.messageoutput.insert(END, "\n\n" + str(test_msg), "tag_username")
                            self.messageoutput.insert(END, " has been ")
                            self.messageoutput.insert(END, "unmuted", "tag_command")
                            self.messageoutput.insert(END, " in your chat.")
                        self.messageoutput.config(state=DISABLED)

                    except:
                        texts = self.messageoutput.get("1.0", END).strip()
                        self.messageoutput.config(state=NORMAL)
                        if len(texts) < 1:
                            self.messageoutput.insert(END, "User not found.")
                        else:
                            self.messageoutput.insert(END, "\n\nUser not found.")
                        self.messageoutput.config(state=DISABLED)
                else:
                    texts = self.messageoutput.get("1.0", END).strip()
                    self.messageoutput.config(state=NORMAL)
                    if len(texts) < 1:
                        self.messageoutput.insert(END, "Command not found.")
                    else:
                        self.messageoutput.insert(END, "\n\nCommand not found.")
                    self.messageoutput.config(state=DISABLED)
            else:
                texts = self.messageoutput.get("1.0", END).strip()
                self.messageoutput.config(state=NORMAL)
                if len(texts) < 1:
                    self.messageoutput.insert(END, "You >> ", "tag_your_message")
                    self.messageoutput.insert(END, msg)
                else:
                    self.messageoutput.insert(END, "\n\nYou >> ", "tag_your_message")
                    self.messageoutput.insert(END, msg)

                self.messageoutput.config(state=DISABLED)
                threading._start_new_thread(self.send_mssage_to_server, (msg, "y"))
                self.sound_sent()

    def send_mssage_to_server(self, msg, y):
        wait = 0
        while True:
            if self.recieving == False:
                if wait != 0:
                    time.sleep(int(wait))
                    wait = 0
                else:
                    threading._start_new_thread(self.send_data, (msg, "s"))
                    break
            if self.recieving == True:
                if wait == 0:
                    wait = (int(self.userid) + 1)


root = Toplevel()
root.option_add("*TCombobox*Listbox*Background", '#12263A')
root.option_add("*TCombobox*Listbox*Foreground", '#63CCCA')
root.option_add("*TCombobox*Listbox*Font", 'Raleway 17')

wmgstyle1 = ttk.Style()
wmgstyle1.theme_create('wmgstyle1', parent = 'alt', settings = {'TCombobox': {'configure': {'fieldbackground': '#63CCCA', 'background': '#12263A', 'foreground': '#12263A', 'arrowcolor': "#63CCCA" , 'arrowsize' : '20', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TEntry': {'configure': {'fieldbackground': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA" }}, 'TButton': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA", 'font': "Raleway 12"}}, 'TScrollbar': {'configure': {'background': "#63CCCA" , 'foreground': '#12263A', 'selectbackground' : '#12263A', 'selectforeground' : "#63CCCA"}}})

wmgstyle1.theme_use("wmgstyle1")

lf = BaseFrame(root)
root.geometry("325x600")
root.iconphoto(False, PhotoImage(file=BaseFrame.icon))
root.title("CTF Chatroom")
root.resizable(False, False)
root.mainloop()
