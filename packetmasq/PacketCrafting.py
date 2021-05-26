import random
from scapy.all import *

valid_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
valid_dec = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def checkMac(mac):
    if len(mac) == 17:
        for x in range(0, len(mac)-1):
            if x == 2 or x == 5 or x == 8 or x == 11 or x == 14:
                if mac[x] != ':':
                    return 0
            else:
                if mac[x].lower() not in valid_hex:
                    return 0
        return 1
    else:
        return 0

def checkIP(ip):
    ip = ip.split(".")
    if len(ip) == 4:
        for x in range(0, len(ip)):
            for y in ip[x]:
                if y not in valid_dec:
                    return 0
                if ip[x] == "0" and (x == 1 or x == 2):
                    pass
                elif ip[x][0] == "0":
                    ip[x] = ip[x][1:]
            if ip[x] == '':
                return 0
            if int(ip[x]) > 255:
                return 0
        print(ip[0] + "." + ip[1] + "." +  ip[2] + "." + ip[3])
        return ip[0] + "." + ip[1] + "." +  ip[2] + "." + ip[3]
    else:
        return 0

def checkPort(port):
    for x in port:
        if x not in valid_dec:
            return 0
        if port[0] == "0":
            port = port[1:]
    if int(port) >= 1 and int(port) < 65536:
        return port
    else:
        return 0

def checkID(id):
    for x in id:
        if x not in valid_dec:
            return 0
        if id[0] == "0":
            id = id[1:]
    if int(id) >= 1000 and int(id) < 10000:
        return id
    else:
        return 0

def checkTime(time):
    for x in time:
        if x not in valid_dec:
            return 0
        if time[0] == "0":
            time = time[1:]
    if int(time) >= 10 and int(time) < 100:
        return time
    else:
        return 0

def checkCount(count):
    for x in count:
        if x not in valid_dec:
            return 0
        if count[0] == "0":
            count = count[1:]
    if int(count) >= 0 and int(count) < 1001:
        return count
    else:
        return 0


while True:
    packet_type = input("Do you want to send; TCP, UDP, ICMP?\n>> ")
    if packet_type.lower() == "tcp":
        type_insert = "TCP"
        break
    if packet_type.lower() == "udp":
        type_insert = "UDP"
        break
    if packet_type.lower() == "icmp":
        type_insert = "ICMP"
        break
    else:
        pass
    
while True:
    mac_choice = input("Do you want to change the sender mac address; yes, no\n>> ")
    if mac_choice.lower() == "yes":
        mac_address = input("Please enter valid mac address; 00:00:00:00:00:00\n>> ")
        if checkMac(mac_address) == 0:
            print("Not valid mac address")
        else:
            mac_insert = "Ether(src=\"" + mac_address + "\")/"
            break
    if mac_choice.lower() == "no":
        mac_insert = ''
        break
                
while True:
    source_ip_choice = input("Do you want to change the source ip address; yes, no\n>> ")
    if source_ip_choice.lower() == "yes":
        source_ip_address = input("Please enter valid ip address; 0.0.0.0\n>> ")
        source_ip_address = checkIP(source_ip_address)
        if source_ip_address == 0:
            print("Not valid ip address")
        else:
            source_ip_insert = "src=\"" + source_ip_address + '"'
            break
    if source_ip_choice.lower() == "no":
        source_ip_insert = ''
        break

while True:
    destination_ip_choice = input("Do you want to change the destination ip address; yes, no\n>> ")
    if destination_ip_choice.lower() == "yes":
        destination_ip_address = input("Please enter valid ip address; 0.0.0.0\n>> ")
        destination_ip_address = checkIP(destination_ip_address)
        if destination_ip_address == 0:
            print("Not valid ip address")
        else:
            destination_ip_insert = "dst=\"" + destination_ip_address + '"'
            break
    if destination_ip_choice == "no":
        print("You must enter a destination address")

if packet_type.lower() == "tcp" or packet_type.lower() == "udp":
    while True:
        source_port_choice = input("Do you want to change the source port; yes, no, random\n>> ")
        if source_port_choice.lower() == "yes":
            source_port = input("Please enter valid port; 1-65535\n>> ")
            source_port = checkPort(source_port)
            if source_port == 0:
                print("Not valid port")
            else:
                source_port_insert = "sport=" + str(source_port)
                break
        if source_port_choice.lower() == "random":
            source_port = RandShort()
            source_port_insert = "sport=" + str(source_port)
            break
        if source_port_choice.lower() == "no":
            source_port_insert = ''
            break

    while True:
        destination_port_choice = input("Do you want to change the destination port; yes, no\n>> ")
        if destination_port_choice.lower() == "yes":
            destination_port = input("Please enter valid port; 1-65535\n>> ")
            destination_port = checkPort(destination_port)
            if destination_port == 0:
                print("Not valid port")
            else:
                destination_port_insert = "dport=" + str(destination_port)
                break
        if destination_port_choice.lower() == "no":
            destination_port_insert = ''
            break

    while True:
        flag_choice = input("Do you want to chose the packet flags; SYN, SYN ACK, ACK, FIN, FIN ACK\n>> ")
        flag = ''
        if flag_choice.lower() == "syn":
            flag = "S"
        if flag_choice.lower() == "syn ack":
            flag = "SA"
        if flag_choice.lower() == "ack":
            flag = "A"
        if flag_choice.lower() == "fin":
            flag = "F"
        if flag_choice.lower() == "fin ack":
            flag = "FA"
        if flag != '':
            flag_insert = "flags='" + flag + "'"
            break

while True:
    packet_id_choice = input("Do you want to chose the packet id; yes, no, random\n>> ")
    if packet_id_choice.lower() == "yes":
        packet_id = input("Please enter valid id; 1000-9999\n>> ")
        packet_id = checkID(packet_id)
        if packet_id == 0:
            print("Not valid id")
        else:
            packet_id_insert = "id=" + str(packet_id)
            break
    if packet_id_choice.lower() == "random":
        packet_id = random.randint(1000, 9999)
        packet_id_insert = "id=" + str(packet_id)
        break
    if packet_id_choice.lower() == "no":
        packet_id_insert = ''
        break

while True:
    packet_time_choice = input("Do you want to chose the packet time to live; yes, no, random\n>> ")
    if packet_time_choice.lower() == "yes":
        packet_time = input("Please enter valid time; 10-99\n>> ")
        packet_time = checkTime(packet_time)
        if packet_time == 0:
            print("Not valid time")
        else:
            time_insert = "ttl=" + str(packet_time)
            break
    if packet_time_choice.lower() == "random":
        packet_time = random.randint(10, 99)
        time_insert = "ttl=" + str(packet_time)
        break
    if packet_time_choice.lower() == "no":
        time_insert = ''
        break

while True:
    packet_count_choice = input("Do you want to chose the number of packets to be sent; yes, no, random\n>> ")
    if packet_count_choice.lower() == "yes":
        packet_count = input("Please enter valid number; 1-1000\n>> ")
        packet_count = checkCount(packet_count)
        if packet_count == 0:
            print("Not valid number")
        else:
            count_insert = "count=" + str(packet_count)
            break
    if packet_count_choice.lower() == "random":
        packet_count = random.randint(1, 1000)
        count_insert = "count=" + str(packet_count)
        break
    if packet_count_choice.lower() == "no":
        count_insert = ''
        break

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

if packet_type.lower() == "tcp" or packet_type.lower() == "udp":
    packet += source_port_insert

    if destination_port_insert != '':
        packet += ", " + destination_port_insert

    if packet_type.lower() == "tcp":
        if flag_insert != '':
            packet += ", " + flag_insert

packet += ')'

if count_insert != '':
    packet += ", " + count_insert

print(packet)

if mac_insert != '':
    os.system('python -m scapy')
    os.system("send(" + packet + ")")
else:
    os.system('python -m scapy')
    os.system("send(" + packet + ")")




