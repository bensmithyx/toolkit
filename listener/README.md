# Reverse shell tool

## Usage
```python
python reverse.py
```

## How it works
This tool will ask the user to enter their IP address, a port of choice and a language which they would like reverse shell code for. It will then output the reverse shell code for the user to choose from and when chosen, a listener will be run and reverse shell code will be output to the screen so that the user can copy and paste this code into the victim machine to start a reverse shell connection. Other tools can then be used to escalate privilege etc.

Languages supported:
- Bash (tcp)
- Perl
- Python
- PHP
- Ruby
- Golang
- Netcat
- Ncat
- Powershell
- TCLsh
- Gawk
- Telnet