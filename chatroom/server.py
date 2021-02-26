import tkinter as tk
import socket
import threading

import datetime, time, sys, subprocess, math

alphabet = [' ', '!', 'w', 's', 'o', 'k', 'g', 'c', '.', 'z', 'v', 'r', 'n', 'j', 'f', 'b', ',', 'y', 'u', 'q', 'm', 'i', 'e', 'a', '?', 'x', 't', 'p', 'l', 'h', 'd', '>', '}', ')', '^', '£', '+', '\\', ';', '7', '3', 'Y', 'U', 'Q', 'M', 'I', 'E', 'A', '<', '{', '(', '%', '@', '-', '"', '0', '6', '2', 'X', 'T', 'P', 'L', 'H', 'D', '~', ']', '*', '$', '_', '/', "'", '9', '5', '1', 'W', 'S', 'O', 'K', 'G', 'C', '`', '[', '&', '#', '=', '|', ':', '8', '4', 'Z', 'V', 'R', 'N', 'J', 'F', 'B']
x = datetime.datetime.now()
year = x.year
month = x.month
day = x.day

def encode_binary(value):
    bits = 128 - value
    num = '{0:b}'.format(bits)
    while len(num) < 7:
        num = "0%s" % num
    num = "11%s" % num
    return num

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

def send_data(c, data):
    global setting
    c.send("1".encode())
    c.send("2".encode())
    for d in data:
        for s in encode_binary(setting.index(d)):
            c.send("2".encode())
            time.sleep((float(s) + 1) / 10)
    c.send("2".encode())
    c.send("3".encode())

def encode_data(data):
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

setting = shift(day, month, year)


window = tk.Tk()
window.title("Sever")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST_ADDR = "localhost"
HOST_PORT = 25215
client_name = " "
clients = []
clients_names = []


# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append(client)

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client, addr))


# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = " "
    # send welcome message to client
    username_data = []
    while True:
        t1 = time.time()
        name_data  = client_connection.recv(1)
        name_data = name_data.decode("utf-8")
        if int(name_data) == 2:
            t0 = time.time()
            data = math.trunc((float(t0-t1)*10))
            #binarychar = int(round_down((float(t0-t1) * 10),0) )
            #print(binarychar)
            username_data.append(data)
        if int(name_data) == 3:
            break
    username_data = username_data[2:]
    client_name = decode_data(decode_binary(username_data))
    username_data = []
    
    client_connection.send("4".encode())
    clients_names.append(client_name)
    update_client_names_display(clients_names)  # update client names display

    message_data = []
    while True:
        client_msg = client_connection.recv(1)
        for c in clients:
            if c != client_connection:
                c.send(client_msg)
        if not client_msg:
            break
        
    idx = get_client_index(clients, client_connection)
    sending_client_name = clients_names[idx]
        
    for c in clients:
        if c != client_connection:
            c.send("6".encode())
            send_data(c, sending_client_name)

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)  # update client names display


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()
