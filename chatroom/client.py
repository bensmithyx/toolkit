# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import socket
import threading

import datetime, time, sys, subprocess, math

alphabet = [' ', '!', 'w', 's', 'o', 'k', 'g', 'c', '.', 'z', 'v', 'r', 'n', 'j', 'f', 'b', ',', 'y', 'u', 'q', 'm', 'i', 'e', 'a', '?', 'x', 't', 'p', 'l', 'h', 'd', '>', '}', ')', '^', '£', '+', '\\', ';', '7', '3', 'Y', 'U', 'Q', 'M', 'I', 'E', 'A', '<', '{', '(', '%', '@', '-', '"', '0', '6', '2', 'X', 'T', 'P', 'L', 'H', 'D', '~', ']', '*', '$', '_', '/', "'", '9', '5', '1', 'W', 'S', 'O', 'K', 'G', 'C', '`', '[', '&', '#', '=', '|', ':', '8', '4', 'Z', 'V', 'R', 'N', 'J', 'F', 'B']
x = datetime.datetime.now()
year = x.year
month = x.month
day = x.day

window = tk.Tk()
window.title("Client")
username = " "
userid = 'i'
users = ['', '', '', '', '', '', '', '', '', '']

topFrame = tk.Frame(window)
lblName = tk.Label(topFrame, text = "Name:").pack(side=tk.LEFT)
entName = tk.Entry(topFrame)
entName.pack(side=tk.LEFT)
btnConnect = tk.Button(topFrame, text="Connect", command=lambda : connect())
btnConnect.pack(side=tk.LEFT)
#btnConnect.bind('<Button-1>', connect)
topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
lblLine = tk.Label(displayFrame, text="*********************************************************************").pack()
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="blue")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
displayFrame.pack(side=tk.TOP)


bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="grey", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)


def connect():
    global username, client
    if len(entName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        username = entName.get()
        connect_to_server(username)


# network client
client = None
HOST_ADDR = "localhost"
HOST_PORT = 2521

def decode_binary(data):
    nums = []
    out = []
    count = 0
    temp = ""
    for b in data:
        if count == 0:
            count += 1
            pass
        else:
            temp += str(b)
            count += 1
            if count == 9:
                nums.append(int(temp))
                temp = ""
                count = 0
    for n in nums:
        num = 256 - int(str(n), 2)
        if num < 96:
            out.append(num)
    return out


def encodebinary(value):
    bits = 128 - value
    num = '{0:b}'.format(bits)
    while len(num) < 7:
        num = "0%s" % num
    num = "11%s" % num
    return num

def check(out, new, x):
    if out[new] == '':
        out[new] = x
        return out
    else:
        check(out, new+1, x)

def shift(day, month, year):
    shift = ((day**2) + month) * year
    out = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
    for x in range(0, len(alphabet)):
        z = len(alphabet) - x
        new = shift % z
        check(out, new, alphabet[x])
    return out
    
def encodedata(data):
    global setting
    outputlist = []
    for d in data:
        newloc = alphabet.index(d)
        outputlist.append(setting[newloc])
    output = "".join(outputlist)
    return output

def decode_data(data):
    global setting
    outputlist = []
    for d in data:
        outputlist.append(setting[d])
    output = "".join(outputlist)
    return output

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    rounded = math.floor(n * multiplier) / multiplier
    return rounded

def send_data(data):
    global client, setting, userid
    client.send("s".encode())
    client.send(str(userid).encode())
    for d in data:
        for s in encodebinary(setting.index(str(d))):
            client.send(str(userid).encode())
            time.sleep((float(s) + 1) / 10)
    client.send(str(userid).encode())
    client.send("f".encode())

setting = shift(day, month, year)

def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, userid
    #try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST_ADDR, HOST_PORT))
    send_data(name)
    id_data = []
    while True:
        server_userid = client.recv(1)
        server_userid = server_userid.decode("utf-8")
        if str(server_userid) == "n":
            server_userid = client.recv(1)
            userid = server_userid.decode("utf-8")
            server_fin = client.recv(1)
            break

    if userid:
        output_message = "Welcome " + username + ". Please type 'exit' to quit"
        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            tkDisplay.insert(tk.END, output_message)
        else:
            tkDisplay.insert(tk.END, "\n\n" + output_message)

        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)

    entName.config(state=tk.DISABLED)
    btnConnect.config(state=tk.DISABLED)
    tkMessage.config(state=tk.NORMAL)

    # start a thread to keep receiving message from server
    # do not block the main thread :)
    threading._start_new_thread(receive_message_from_server, (client, "m"))
    #except Exception as e:
        #tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")


def receive_message_from_server(sck, m):
    global username, userid, users
    while True:
        from_server = sck.recv(1)
        from_server = from_server.decode("utf-8")
        print(from_server)
        message_data = []
        user_data = []
        leave_data = []
        change_data = []
        while True:
            t1 = time.time()
            server_data  = sck.recv(1)
            print(server_data)
            if str(from_server) == "u":
                server_data = server_data.decode("utf-8")
                if str(server_data) == "f":
                    del user_data[0:2]
                    user_name = decode_data(decode_binary(user_data))
                    users[int(id_data)] = user_name
                    output_message = str(user_name) + " has joined the chat."
                    texts = tkDisplay.get("1.0", tk.END).strip()
                    tkDisplay.config(state=tk.NORMAL)
                    if len(texts) < 1:
                        tkDisplay.insert(tk.END, output_message)
                    else:
                        tkDisplay.insert(tk.END, "\n\n" + output_message)

                    tkDisplay.config(state=tk.DISABLED)
                    tkDisplay.see(tk.END)
                    user_data = []
                    break
                
                t0 = time.time()
                data = int(round_down(t0-t1,2) * 10)
                if data != 0:
                    data -= 1
                user_data.append(data)
                id_data = server_data.decode("utf-8")
                
            if str(from_server) == "l":
                server_data = server_data.decode("utf-8")
                if str(server_data) == "f":
                    output_message = str(users[int(leave_data[0])]) + " has left the chat."
                    texts = tkDisplay.get("1.0", tk.END).strip()
                    tkDisplay.config(state=tk.NORMAL)
                    if len(texts) < 1:
                        tkDisplay.insert(tk.END, output_message)
                    else:
                        tkDisplay.insert(tk.END, "\n\n" + output_message)
                    tkDisplay.config(state=tk.DISABLED)
                    tkDisplay.see(tk.END)
                    break
                
                leave_data.append(str(server_data))

            if str(from_server) == "c":
                server_data = server_data.decode("utf-8")
                if str(server_data) == "f":
                    output_message = str(users[int(change_data[1])]) + " has left the chat."
                    texts = tkDisplay.get("1.0", tk.END).strip()
                    tkDisplay.config(state=tk.NORMAL)
                    if len(texts) < 1:
                        tkDisplay.insert(tk.END, output_message)
                    else:
                        tkDisplay.insert(tk.END, "\n\n" + output_message)
                    tkDisplay.config(state=tk.DISABLED)
                    tkDisplay.see(tk.END)
                    
                    if int(userid) == int(change_data[0]):
                        userid = int(change_data[1])
                        change_data = []
                        break
                    else:
                        users[int(change_data[1])] = users[int(change_data[0])]
                        users[int(change_data[0])] = ''
                        change_data = []
                        break
                change_data.append(str(server_data))

            if str(from_server) == "s":
                server_data = server_data.decode("utf-8")
                if str(server_data) == "f":
                    del message_data[0:2]
                    server_message = decode_data(decode_binary(message_data))
                    output_message = str(users[int(id_data)]) + " >> " + server_message

                    texts = tkDisplay.get("1.0", tk.END).strip()
                    tkDisplay.config(state=tk.NORMAL)
                    if len(texts) < 1:
                        tkDisplay.insert(tk.END, output_message)
                    else:
                        tkDisplay.insert(tk.END, "\n\n"+ output_message)

                    tkDisplay.config(state=tk.DISABLED)
                    tkDisplay.see(tk.END)
                    message_data = []
                    break
                
                t0 = time.time()
                data = int(round_down(t0-t1,2) * 10)
                if data != 0:
                    data -= 1
                message_data.append(data)
                id_data = server_data.decode("utf-8")

    sck.close()
    window.destroy()


def getChatMessage(msg):

    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()

    # enable the display area and insert the text and then disable.
    # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You >> " + msg, "tag_your_message") # no line
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You >> " + msg, "tag_your_message")

    tkDisplay.config(state=tk.DISABLED)

    send_mssage_to_server(msg)

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)


def send_mssage_to_server(msg):
    send_data(msg)
    
    if msg == "exit":
        client.close()
        window.destroy()


window.mainloop()
