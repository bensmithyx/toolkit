#!/bin/env python3
import os, sys, subprocess, string, random

bashfile=''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(10))#creates a random 10 character alphanumeric string to name the .sh
bashfile='/tmp/'+bashfile+'.sh'#store .sh in the tmp directory
f = open(bashfile, 'w')#opens the .sh file just created 
s = """#!/bin/sh
xdotool type '#################'
xdotool key Return
xdotool type 'unset HISTFILE'
xdotool key Return
xdotool type 'python -c '\\''import pty; pty.spawn("/bin/bash")'\\'' || python3 -c '\\''import pty; pty.spawn("/bin/bash")'\\'' || script -qc /bin/bash /dev/null'
xdotool key Return
xdotool keydown ctrl key z; sleep .1; xdotool keyup ctrl
xdotool type 'stty size | xclip -selection clipboard'
xdotool key Return
xdotool type 'stty raw -echo; fg'
xdotool key Return
xdotool type 'unset HISTFILE'
xdotool key Return
xdotool type 'export SHELL=bash'
xdotool key Return
xdotool type 'export TERM=xterm-256color'
xdotool key Return
xdotool type "stty cols $(xclip -o -selection clipboard | awk '{print $2}') rows $(xclip -o -selection clipboard | awk '{print $1}')"
xdotool key Return
xdotool type 'reset'
xdotool key Return
xdotool type 'exec /bin/bash'
xdotool key Return
xdotool type 'clear'
xdotool key Return
"""#store shell code in the variable "s"
f.write(s)#write contents of "s" to the .sh
f.close()#close the .sh
os.chmod(bashfile, 0o755)#make the .sh executable
subprocess.call(bashfile, shell=True)#run the shell script
