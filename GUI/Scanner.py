from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from scapy.all import *
import threading, os, subprocess, sys, re, getopt, signal, socket, requests, time

class Dirb:
    def __init__(self,files,host):
        self.files = files
        self.host = host

class Scan:
    def __init__(self,ports,statuses,services,host,time):
        self.ports = ports
        self.statuses = statuses
        self.services = services
        self.host = host
        self.time = time

#this is the GUI code - creating the template. This is common across all, with the exception of labels/buttons in different areas.
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

    	self.IPtitle = Label(self.main, text="Destination IP:", fg="#63CCCA", bg="#12263A", font="Raleway 24", pady="10", padx = "20")

    	self.filetitle = Label(self.main, text="Filename:", fg="#63CCCA", bg="#12263A", font="Raleway 24", pady="10", padx = "20")

    	self.IPtitle.grid(row = 0, column = 0)
    	self.filetitle.grid(row = 0, column = 1)

    	self.IPentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")
    	self.fileentrybg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")
    	self.scanbuttonbg = Frame(self.main, bg="#12263A", borderwidth = 0, relief = SUNKEN, pady="10", padx = "20")

    	self.IPentrybg.grid(row = 1, column = 0)
    	self.fileentrybg.grid(row = 1, column = 1)
    	self.scanbuttonbg.grid(row = 1, column = 2, columnspan = 2)

    	self.scanoutput = Text(self.main, bg="#12263A", fg='#63CCCA', width = 72, height = 10, borderwidth = 1, relief = SUNKEN, font="Raleway 14")
    	self.scanoutput.grid(row = 2, column = 0, columnspan = 3)
    	self.scanoutput.config(state = DISABLED)

    	self.outscroll = ttk.Scrollbar(self.main, command=self.scanoutput.yview)
    	self.outscroll.grid(row=2, column=2, sticky='nse')
    	self.scanoutput['yscrollcommand'] = self.outscroll.set

    	self.v = StringVar()
    	self.IPentry = ttk.Entry(self.IPentrybg, textvariable = self.v, font="Raleway 24", width = 15)
    	self.IPentry.grid(row = 0, column = 0)

    	self.z = StringVar()
    	self.fileentry= ttk.Entry(self.fileentrybg, textvariable = self.z, font="Raleway 24", width = 12)
    	self.fileentry.grid(row = 0, column = 0)

    	self.scanbutton = ttk.Button(self.scanbuttonbg, text = "Scan", width = 6, command = self.scan_btn_pressed)
    	self.scanbutton.grid(row = 0, column = 0)

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

    	sys.stdout = TextRedirector(self.scanoutput, "stdout")
    	sys.stderr = TextRedirector(self.scanoutput, "stderr")

    	self.pack()

    valid_hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    valid_dec = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    scans = []
    dirbslist = []

#this checks if the IP entered is a valid IP address
    def checkIP(self, ip):
        if ip == "localhost":
            return ip
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

    def servicescan(self, port, protocal):
        try:
            service = socket.getservbyport(port, protocal)
            return service
        except:
            return False

    def readfile(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()
        file.close()
        return lines


    def scanner(self, ip, portranges):
        top_20_ports = [20,21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,8000]
        top_1000_ports = [1,3,4,6,7,9,13,17,19,20,21,22,23,24,25,26,30,32,33,37,42,43,49,53,70,79,80,81,82,83,84,85,88,89,90,99,100,106,109,110,111,113,119,125,135,139,143,144,146,161,163,179,199,211,212,222,254,255,256,259,264,280,301,306,311,340,366,389,406,407,416,417,425,427,443,444,445,458,464,465,481,497,500,512,513,514,515,524,541,543,544,545,548,554,555,563,587,593,616,617,625,631,636,646,648,666,667,668,683,687,691,700,705,711,714,720,722,726,749,765,777,783,787,800,801,808,843,873,880,888,898,900,901,902,903,911,912,981,987,990,992,993,995,999,1000,1001,1002,1007,1009,1010,1011,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031,1032,1033,1034,1035,1036,1037,1038,1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1059,1060,1061,1062,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1075,1076,1077,1078,1079,1080,1081,1082,1083,1084,1085,1086,1087,1088,1089,1090,1091,1092,1093,1094,1095,1096,1097,1098,1099,1100,1102,1104,1105,1106,1107,1108,1110,1111,1112,1113,1114,1117,1119,1121,1122,1123,1124,1126,1130,1131,1132,1137,1138,1141,1145,1147,1148,1149,1151,1152,1154,1163,1164,1165,1166,1169,1174,1175,1183,1185,1186,1187,1192,1198,1199,1201,1213,1216,1217,1218,1233,1234,1236,1244,1247,1248,1259,1271,1272,1277,1287,1296,1300,1301,1309,1310,1311,1322,1328,1334,1352,1417,1433,1434,1443,1455,1461,1494,1500,1501,1503,1521,1524,1533,1556,1580,1583,1594,1600,1641,1658,1666,1687,1688,1700,1717,1718,1719,1720,1721,1723,1755,1761,1782,1783,1801,1805,1812,1839,1840,1862,1863,1864,1875,1900,1914,1935,1947,1971,1972,1974,1984,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2013,2020,2021,2022,2030,2033,2034,2035,2038,2040,2041,2042,2043,2045,2046,2047,2048,2049,2065,2068,2099,2100,2103,2105,2106,2107,2111,2119,2121,2126,2135,2144,2160,2161,2170,2179,2190,2191,2196,2200,2222,2251,2260,2288,2301,2323,2366,2381,2382,2383,2393,2394,2399,2401,2492,2500,2522,2525,2557,2601,2602,2604,2605,2607,2608,2638,2701,2702,2710,2717,2718,2725,2800,2809,2811,2869,2875,2909,2910,2920,2967,2968,2998,3000,3001,3003,3005,3006,3007,3011,3013,3017,3030,3031,3052,3071,3077,3128,3168,3211,3221,3260,3261,3268,3269,3283,3300,3301,3306,3322,3323,3324,3325,3333,3351,3367,3369,3370,3371,3372,3389,3390,3404,3476,3493,3517,3527,3546,3551,3580,3659,3689,3690,3703,3737,3766,3784,3800,3801,3809,3814,3826,3827,3828,3851,3869,3871,3878,3880,3889,3905,3914,3918,3920,3945,3971,3986,3995,3998,4000,4001,4002,4003,4004,4005,4006,4045,4111,4125,4126,4129,4224,4242,4279,4321,4343,4443,4444,4445,4446,4449,4550,4567,4662,4848,4899,4900,4998,5000,5001,5002,5003,5004,5009,5030,5033,5050,5051,5054,5060,5061,5080,5087,5100,5101,5102,5120,5190,5200,5214,5221,5222,5225,5226,5269,5280,5298,5357,5405,5414,5431,5432,5440,5500,5510,5544,5550,5555,5560,5566,5631,5633,5666,5678,5679,5718,5730,5800,5801,5802,5810,5811,5815,5822,5825,5850,5859,5862,5877,5900,5901,5902,5903,5904,5906,5907,5910,5911,5915,5922,5925,5950,5952,5959,5960,5961,5962,5963,5987,5988,5989,5998,5999,6000,6001,6002,6003,6004,6005,6006,6007,6009,6025,6059,6100,6101,6106,6112,6123,6129,6156,6346,6389,6502,6510,6543,6547,6565,6566,6567,6580,6646,6666,6667,6668,6669,6689,6692,6699,6779,6788,6789,6792,6839,6881,6901,6969,7000,7001,7002,7004,7007,7019,7025,7070,7100,7103,7106,7200,7201,7402,7435,7443,7496,7512,7625,7627,7676,7741,7777,7778,7800,7911,7920,7921,7937,7938,7999,8000,8001,8002,8007,8008,8009,8010,8011,8021,8022,8031,8042,8045,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8093,8099,8100,8180,8181,8192,8193,8194,8200,8222,8254,8290,8291,8292,8300,8333,8383,8400,8402,8443,8500,8600,8649,8651,8652,8654,8701,8800,8873,8888,8899,8994,9000,9001,9002,9003,9009,9010,9011,9040,9050,9071,9080,9081,9090,9091,9099,9100,9101,9102,9103,9110,9111,9200,9207,9220,9290,9415,9418,9485,9500,9502,9503,9535,9575,9593,9594,9595,9618,9666,9876,9877,9878,9898,9900,9917,9929,9943,9944,9968,9998,9999,10000,10001,10002,10003,10004,10009,10010,10012,10024,10025,10082,10180,10215,10243,10566,10616,10617,10621,10626,10628,10629,10778,11110,11111,11967,12000,12174,12265,12345,13456,13722,13782,13783,14000,14238,14441,14442,15000,15002,15003,15004,15660,15742,16000,16001,16012,16016,16018,16080,16113,16992,16993,17877,17988,18040,18101,18988,19101,19283,19315,19350,19780,19801,19842,20000,20005,20031,20221,20222,20828,21571,22939,23502,24444,24800,25734,25735,26214,27000,27352,27353,27355,27356,27715,28201,30000,30718,30951,31038,31337,32768,32769,32770,32771,32772,32773,32774,32775,32776,32777,32778,32779,32780,32781,32782,32783,32784,32785,33354,33899,34571,34572,34573,35500,38292,40193,40911,41511,42510,44176,44442,44443,44501,45100,48080,49152,49153,49154,49155,49156,49157,49158,49159,49160,49161,49163,49165,49167,49175,49176,49400,49999,50000,50001,50002,50003,50006,50300,50389,50500,50636,50800,51103,51493,52673,52822,52848,52869,54045,54328,55055,55056,55555,55600,56737,56738,57294,57797,58080,60020,60443,61532,61900,62078,63331,64623,64680,65000,65129,65389]
        if portranges == "top-20-ports":
            portrange = top_20_ports
        elif portranges == "all-ports":
            portrange = list(range(65535))
        elif portranges == "top-1000-ports":
            portrange = top_1000_ports
        else:
            display("Invalid range set")
            return 0
        # Creating arrays for ips of the ports, status of the ports and service of the ports to be populated with
        ports, statuses, services = [],[],[]
        try:
            print("Scanning (" + ip + ")")
            # Scanning all ports 65535
            t1 = datetime.now()
            for port in portrange:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    ports.append(port)
                    statuses.append("open")
                    # If service is not found using tcp or udp it will be unknown
                    service = self.servicescan(port,"tcp")
                    if not service:
                        # If the service is not found for tcp or udp is will set service as unknown
                        if not self.servicescan(port,"udp"):
                            services.append("Unknown")
                    else:
                        services.append(service)
                sock.close()
            t2 = datetime.now()
            self.scans.append(Scan(ports,statuses,services,ip,t2-t1))
        # If ctrl+c is pressed it will display "Exited"
        except KeyboardInterrupt:
            print("Exiting")
            sys.exit()
        except socket.gaierror:
            print('Hostname could not be resolved.')
            sys.exit()
        except socket.error:
            print("Couldn't connect to server")
            sys.exit()

    def requestweb(self, type, ip, port, words, start):
        files = []
        recursivecheck = False
        globaltype[0] = type
        spaces = 0
        for word in words:
            word = word.strip()
            if start != "None":
                word = f"{start}/{word}"
            formattedword = word+(" "*spaces)
            spaces = len(word)
            #print(f"{type}://{ip}:{port}/{formattedword}", end="\r")
            r = requests.get(f"{type}://{ip}:{port}/{word}")
            if r.status_code in [200,403]:
                # Checking if it is a file or directory
                try:
                    recursive = requests.get(f"{type}://{ip}:{port}/{word}/")
                    if recursive.status_code in [200,403]:
                        recursivecheck = True
                except:
                    pass
                if r.status_code == 200:
                    # Formating output for cli and save file for 200 codes
                    files.append("{}://{}:{}/{}{}200".format(type, ip, port, word, (" "*(25-len(word)))))
                    print("{}://{}:{}/{}{}200".format(type, ip, port, word, (" "*(25-len(word)))))
                elif r.status_code == 403:
                    # Formating output for cli and save file for 403 codes
                    files.append("{}://{}:{}/{}{}403".format(type, ip, port, word, (" "*(25-len(word)))))
                    print("{}://{}:{}/{}{}403".format(type,ip, port, word, (" "*(25-len(word)))))
                if recursivecheck:
                    self.requestweb(type, ip, port, words, word)
        # Clearing last output
        self.dirbslist.append(Dirb(files,ip))

    def scan_btn_pressed(self):
        filename = self.fileentry.get()
        userip = self.IPentry.get()
        ip = self.checkIP(userip)
        wordlist = "common.txt"
        portrange = "top-1000-ports"
        if ip != 0:
                #
                # Displaying output of host scan to the user.
                # Scanning all ports
                # Running host scan
            self.scanner(ip,portrange)
            print(f"PORT    STATUS    SERVICE\n")
                # Displaying output to cli and sotring output into a temp file in case it wants to be saved
            for port, status, service in zip(self.scans[-1].ports,self.scans[-1].statuses,self.scans[-1].services):
                print(str(port) + ' '*(12-len(str(port))) + str(status) + ' '*(14-len(str(status))) + str(service))
            print(f"\nScantime - {self.scans[-1].time}")

            if self.scans:
                for p in range(0, len(self.scans[-1].ports)):
                    if int(self.scans[-1].ports[p]) == 80 or int(self.scans[-1].ports[p]) == 8000 or int(self.scans[-1].ports[p]) == 8080 or int(self.scans[-1].ports[p]) == 443:
                        print("\nScanning Port: " + str(self.scans[-1].ports[p]))
                        choice = p
                        # Reading words from chosen wordlist
                        words = self.readfile(f"wordlists/{wordlist}")
                        global globaltype
                        globaltype = ["none"]
                        # Checking if host:port is valid and will then enumerate
                        try:
                            if requests.get(f"https://{ip}:{self.scans[-1].ports[choice]}/").status_code == 200:
                                self.requestweb("https", ip, self.scans[-1].ports[choice], words, "None")
                        except:
                            try:
                                if requests.get(f"http://{ip}:{self.scans[-1].ports[choice]}/").status_code == 200:
                                    self.requestweb("http", ip, self.scans[-1].ports[choice], words, "None")
                            except Exception as exception:
                                print(exception)
                                print("Port not scannable")
                        print("Scan Complete")


                if filename != "":
                    file = open(filename + ".scan","w")
                    file.write(f"{self.scans[-1].host}-{portrange}.scan")
                    file.write(f"\nPORT    STATUS    SERVICE\n")
                    for port, status, service in zip(self.scans[-1].ports,self.scans[-1].statuses,self.scans[-1].services):
                        file.write(f"\n{port}{' '*(8-len(str(port)))}{status}{' '*(10-len(str(status)))}{service}\n{30*'-'}")
                    file.write(f"\nScantime - {self.scans[-1].time}")
                    file.close()
            else:
                print("Please scan a host first")


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

#This is the common theme across all menus
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
