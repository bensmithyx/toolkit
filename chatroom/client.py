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
HOST_PORT = 25215

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
        out.append(256 - int(str(n), 2))
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
    global client, setting
    client.send("1".encode())
    client.send("2".encode())
    for d in data:
        for s in encodebinary(setting.index(d)):
            client.send("2".encode())
            time.sleep((float(s) + 1) / 10)
    client.send("2".encode())
    client.send("3".encode())

setting = shift(day, month, year)

def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        #client.send(name.encode()) # Send name to server after connecting
        send_data(name)

        entName.config(state=tk.DISABLED)
        btnConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")


def receive_message_from_server(sck, m):
    global username
    while True:
        from_server = sck.recv(1)
        message_data = []
        while True:
            broken = 0
            t1 = time.time()
            server_data  = sck.recv(1)
            server_data = server_data.decode("utf-8")
            if int(server_data) == 4:
                broken = 1
                break
            if int(server_data) == 6:
                broken = 2
                break
            if int(server_data) == 2:
                t0 = time.time()
                data = int(round_down(t0-t1,2) * 10)
                if data != 0:
                    data -= 1
                message_data.append(data)
            if int(server_data) == 3:
                break
        if broken == 1:
            server_message = "Welcome "+ username + ". Use 'exit' to quit"
            message_data = []
        if broken == 2:
            server_message = " << "
            message_data = []
        else:
            del message_data[0:2]
            server_message = decode_data(decode_binary(message_data))
            message_data = []

        # display message from server on the chat window

        # enable the display area and insert the text and then disable.
        # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(
        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            tkDisplay.insert(tk.END, server_message)
        else:
            tkDisplay.insert(tk.END, "\n\n"+ server_message)

        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)

        # print("Server says: " +from_server)

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
    #client.send(msg.encode())
    send_data(msg)

    if msg == "exit":
        client.close()
        window.destroy()
    print("Sending message")


window.mainloop()
