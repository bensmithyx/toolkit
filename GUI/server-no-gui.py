# -*- coding: utf-8 -*-
import tkinter as tk
import socket
import threading

import datetime, time, sys, os, subprocess, math

alphabet = [' ', '!', 'w', 's', 'o', 'k', 'g', 'c', '.', 'z', 'v', 'r', 'n', 'j', 'f', 'b', ',', 'y', 'u', 'q', 'm', 'i', 'e', 'a', '?', 'x', 't', 'p', 'l', 'h', 'd', '>', '}', ')', '^', '£', '+', '\\', ';', '7', '3', 'Y', 'U', 'Q', 'M', 'I', 'E', 'A', '<', '{', '(', '%', '@', '-', '"', '0', '6', '2', 'X', 'T', 'P', 'L', 'H', 'D', '~', ']', '*', '$', '_', '/', "'", '9', '5', '1', 'W', 'S', 'O', 'K', 'G', 'C', '`', '[', '&', '#', '=', '|', ':', '8', '4', 'Z', 'V', 'R', 'N', 'J', 'F', 'B']
x = datetime.datetime.now()
year = x.year
month = x.month
day = x.day
kicked = ""
recieving = False
active = False

def encode_binary(value):
    if value == 0:
        num = "18000000"
    else:
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
            if int(b) >= 30:
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
    setting = shift(day, month, year)
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

def send_user_data(client_send, data, userid, prefix):
    global setting
    setting = shift(day, month, year)
    client_send.send(str(prefix).encode())
    client_send.send(str(userid).encode())
    for d in data:
        for s in encode_binary(setting.index(d)):
            client_send.send(str(userid).encode())
            time.sleep(((float(s) * 80) + 1) / 2000)
    client_send.send(str(userid).encode())
    client_send.send("f".encode())

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    rounded = math.floor(n * multiplier) / multiplier
    return rounded

setting = shift(day, month, year)

server = None
HOST_ADDR = "localhost"
#HOST_ADDR = "167.99.199.78"
HOST_PORT = 2521
client_name = " "
clients = []
clients_names = []

def start_server():
    global server, HOST_ADDR, HOST_PORT

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)

    accept_clients(server)

def accept_clients(the_server):
    while True:
        client, addr = the_server.accept()
        clients.append(client)
        threading._start_new_thread(send_receive_client_message, (client, addr))

def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr, recieving, active, kicked
    client_msg = " "
    username_data = []
    count = 0
    while True:
        syn_ack  = client_connection.recv(1)
        syn_ack = syn_ack.decode("utf-8")
        while True:
            if active == False and str(syn_ack) == "x":
                active = True
                client_connection.send("y".encode())
                while True:
                    syn_data  = client_connection.recv(1)
                    syn_data = syn_data.decode("utf-8")
                    if str(syn_data) == "s":
                        if count == 0:
                            for c in clients:
                                 c.send("w".encode())
                            count += 1
                        while True:
                            t1 = time.time()
                            name_data  = client_connection.recv(1)
                            name_data = name_data.decode("utf-8")
                            if str(name_data) == "f":
                                while True:
                                    if recieving == False:
                                        del username_data[0:2]
                                        client_name = decode_data(decode_binary(username_data))
                                        clients_names.append(client_name)
                                        idx = get_client_index(clients, client_connection)
                                        client_connection.send("n".encode())
                                        client_connection.send(str(idx).encode())
                                        client_connection.send("f".encode())
                                        username_data = []
                                        latency_data = []
                                        while True:
                                            t1 = time.time()
                                            client_data = client_connection.recv(1)
                                            t0 = time.time()
                                            data = int(round_down(t0-t1,2) * 2000)
                                            latency_data.append(data)
                                            client_data_test = client_data.decode("utf-8")
                                            if str(client_data_test) == "f":
                                                del latency_data[0:3]
                                                latency_test = decode_data(decode_binary(latency_data))
                                                print(latency_test)
                                                send_user_data(c, latency_test, idx, "p")
                                                latency_data = []
                                            if str(client_data_test) == "q":
                                                print("broken")
                                                break

                                        recieving == True

                                        for c in clients:
                                            if c != client_connection:
                                                send_user_data(c, client_name, idx, "u")
                                            else:
                                                for d in range(0, len(clients_names)):
                                                    if d != idx:
                                                        send_user_data(c, clients_names[d], d, "u")
                                        for c in clients:
                                            c.send("f".encode())
                                        break
                                active = False
                                break
                            t0 = time.time()
                            data = int(round_down(t0-t1,2) * 2000)
                            username_data.append(data)
                        break
                break
        break
    while True:
        try:
            idx = get_client_index(clients, client_connection)
            client_msg = client_connection.recv(1)

            if str(idx) == str(kicked):
                break
            recieving = True
            client_msg_test = client_msg.decode("utf-8")
            if str(client_msg_test) == "r":
                for d in range(0, len(clients_names)):
                    if d != idx:
                        send_user_data(client_connection, clients_names[d], d, "u")

            if str(client_msg_test) == "k":
                client_msg2 = client_connection.recv(1)
                client_msg_test2 = client_msg2.decode("utf-8")
                kicked = client_msg_test2

                clients[int(kicked)].send("b".encode())
                clients[int(kicked)].send(str(kicked).encode())
                clients[int(kicked)].send("f".encode())

            if str(client_msg_test) != "r":
                if str(client_msg_test) != "k":
                    for c in clients:
                        if c != client_connection:
                            c.send(client_msg)
                            
            if str(client_msg_test) == "f":
                recieving = False
                
            if not client_msg:
                recieving = False
                break

        except:
            print("passed")
                    
    just_kicked = False
    old = []

    for o in clients:
        client_idx = get_client_index(clients, o)
        old.append(client_idx)

    if str(kicked) == str(idx):
        for c in clients:
            c.send("k".encode())
            c.send(str(kicked).encode())
            c.send("f".encode())
        kicked = ""
        just_kicked = True
        
    idx = get_client_index(clients, client_connection)

    del clients_names[idx]
    del clients[idx]
    del old[idx]
    client_connection.close()

    if just_kicked == False:
        for c in clients:
            c.send("l".encode())
            c.send(str(idx).encode())
            c.send("f".encode())
        
    for x in range(0, len(old)):
        if int(x) != int(old[x]):
            for c in clients:
                c.send("c".encode())
                c.send(str(old[x]).encode())
                c.send(str(x).encode())
                c.send("f".encode())

def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1
    return idx
    
start_server()
