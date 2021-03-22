#!/bin/env python3
import os
os.system('''
unset HISTFILE
python -c 'import pty; pty.spawn("/bin/bash")' || python3 -c 'import pty; pty.spawn("/bin/bash")' || script -qc /bin/bash /dev/null 
stty size | xclip -selection clipboard
stty raw -echo; fg
unset HISTFILE
export SHELL=bash
export TERM=xterm-256color
stty cols $(xclip -o -selection clipboard | awk '{print $2}') rows $(xclip -o -selection clipboard | awk '{print $1}')
reset
exec /bin/bash
clear
echo done
''')
#first attempt but got stuck trying to make python send ctrl-z signal after line 4. Ended up scrapping this approach and starting fresh in v2
