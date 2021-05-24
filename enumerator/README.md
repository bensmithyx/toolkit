# Enumerator

## Introduction
The enumeration tool will be used to examine a computer to see if there are any common vulnerabilities present that we may be able to exploit.

## Instructions
1. Choose a scan (see the table below), or make your own
2. Decide whether to save the result to a file, or to have it output to the console
3. Wait for the scan to complete
4. If you haved the scan to a file, decide whether to send it to another machine

## What will be scanned and why
### System information
#### OS information
- This allows you to check if the machine is vulnerable to a specific zero-day then it can be used to exploit the system.
#### SUDO version
- This allows you to check if the version of SUDO on the machine has any known vulnerabilities.
#### General system information
- Finds and displays info for things like the printer, CPU, system date etc.
#### Environment variable details
- Searches for any interesting information like passwords or API keys in environment variables.
#### Check defensive measures
- Checks if AppArmor is installed.
- Checks if Grsecurity is installed.
- Checks if PaX is installed.
- Checks if Execshield is installed.
- Checks if SElinux is installed.
- Checks if ASLR is installed.
- All of this allows you to gauge what kind of protections are present or missing on the system, therefore showing you if there are any weak points that can be exploited.
#### Dmesg signature verification failed
- Checks for failed verification. One of the boxes on HTB uses this failure as an exploit.
### Device information
#### Drives
- Displays interesting information about the drives and tells you if they are mounted or unmounted.
Process information
#### Cron jobs belonging to the root user
- Cron jobs are processes that run at specified time intervals
- If the root user is the owner of one of these processes and you can write to the file containing the code that will be executed by the process, you can execute code as though you are the root user, meaning you can do whatever you want.
#### Running processes belonging to the root user
- Displays processes running so we can look for processes which may be running with sudo privileges.
- If you are able to change the code of the process that is being run as root, then you can run your own code as the root user.
#### Timers
- These are systemd unit files that end in .timer.
- They control .service files or events and can be used as an alternative to cron jobs.
- https://book.hacktricks.xyz/linux-unix/privilege-escalation#timers
#### Sockets
- Unix sockets allow communication between two different processes on either the same machine or over a network.
- If you identify a writable socket, then you can communicate with it and possibly exploit a vulnerability, for example, by socket command injection.
- https://www.linux.com/news/what-socket/
- https://book.hacktricks.xyz/linux-unix/privilege-escalation/socket-command-injection
#### D-BUS
- D-BUS is an interprocess communication system that allows applications to communicate with one another.
- If there is a policy that allows a user to interact with the bus, then you can exploit it to escalate privileges.
- https://www.linuxjournal.com/article/7744
### Network information
#### Generic network information
- Displays network information like open ports, IP addresses, MAC addresses, ARP cache and iptables rules.
### User information
#### Information of the current user
- Checking what privileges the account that you are using already has, as well as displaying other account information
#### Information on all users
- Looking at which users are on the system and what privileges these users have
#### SUDO permissions
- Lets you see what things you can do on the machine with root privileges, which you can exploit to become a root user
#### Clipboard and highlighted text
- Checks if there is anything interesting inside the clipboard, for example, passwords
#### PGP keys
- PGP (Pretty Good Privacy) is an encryption program that provides cryptographic privacy and authentication for data communication
- PGP is used for signing, encrypting, and decrypting texts, e-mails, files, directories, and whole disk partitions and to increase the security of e-mail communications
- This means that if something is encrypted using one of these keys, then you can decrypt it and potentially find something that will help you escalate your privileges
- https://cd6629.gitbook.io/ctfwriteups/linux-privesc/tomghost
#### Common password brute force
- Try to brute force a user account using a list of the 500 most commonly used passwords
- The passwords were taken from https://github.com/OWASP/passfault/blob/master/wordlists/wordlists/10k-worst-passwords.txt
### Software information
#### Useful binaries
- Displays info like versions of useful binaries, such as nmap, which may have known vulnerabilities that can be exploited which can be used to escalate privileges.
- https://gtfobins.github.io/ 
#### Screen and TMUX sessions
- You can potentially hijack root owned screen or tmux sessions
### Interesting files
#### Root owned files with SUID or SGID bit set
- If a file has its SUID permission bit set, it means that whatever you do to the file, it will do it as if you are the owner of the file
- This is useful if the owner of the file is the root user, as if the file was executable and you would write to it, you could get your own code executed as though you were the root user
#### Permission bits of sensitive files
- If you are able to read the /etc/shadow file, which by default you can’t do, you will be able to see the hashed passwords of all the users of the computer
- If you are able to write to the /etc/shadow file, you can make your own password, hash it and then set it as the password to a user on the computer, meaning that you have set them a password that you know
- If you are able to write to the /etc/passwd file, you can just remove a users password so that you don’t need to type in a password in order to log in
- https://security.stackexchange.com/questions/151700/privilege-escalation-using-passwd-file
#### Hashes in the /etc/passwd file
- The /etc/passwd file is by default world readable, so if there are hashes in it, you can then try to crack them
#### Path information
- If the user has write permissions inside a folder in the PATH variable then binaries or libraries can be hijacked to do things not intended.
#### List of all hidden files
- Filenames that start with a ‘.’ are hidden in linux
- These hidden files could potentially contain useful information
#### Log files
- If you are able to view the log files on a machine, then you may be able to uncover some interesting or confidential information inside them, including passwords
- https://book.hacktricks.xyz/linux-unix/privilege-escalation#logs
#### List of all writable files
- Being able to write to certain files allows you to escalate privileges
- An example is python library hijacking, which is where if you know where a python script is going to be executed and you can write inside that folder, or if you can modify python libraries, then you can modify the os library  and backdoor it
- https://book.hacktricks.xyz/linux-unix/privilege-escalation#writable-files
#### List of recently modified files
- Recently modified files may contain information that you can use
#### Search files that contain passwords
- Searching files that might contain passwords, which you might be able to use to log in to accounts with higher privileges 
#### List files with unexpected ACL
- This can highlight seemingly unimportant files that may have a stricter ACL than expected because they contain private information

## Types of scan

|             Scan Modules             | Light Scan | Medium Scan | Full Scan |
|:------------------------------------:|:----------:|:-----------:|:---------:|
|                OS Info               |     - [x]    |     - [x]     |    - [x]    |
|             SUDO Version             |     [x]    |     [x]     |    [x]    |
|       Environment Variable Info      |     [x]    |     [x]     |    [x]    |
|        Defensive Measures Info       |            |     [x]     |    [x]    |
|              DMesg Info              |     [x]    |     [x]     |    [x]    |
|              Device Info             |            |     [x]     |    [x]    |
|             Cron Job Info            |            |     [x]     |    [x]    |
|        Running Processes Info        |            |     [x]     |    [x]    |
|              Timers Info             |            |             |    [x]    |
|              Socket Info             |            |     [x]     |    [x]    |
|              D-BUS Info              |            |     [x]     |    [x]    |
|             Network Info             |            |     [x]     |    [x]    |
|         Info on Current User         |     [x]    |     [x]     |    [x]    |
|           Info on All Users          |     [x]    |     [x]     |    [x]    |
|           SUDO Permissions           |     [x]    |     [x]     |    [x]    |
|    Clipboard and Highlighted Text    |            |     [x]     |    [x]    |
|               PGP Keys               |            |             |    [x]    |
|      Common Password Brute Force     |            |             |    [x]    |
|       Useful Binaries Installed      |     [x]    |     [x]     |    [x]    |
|       Screen and TMUX Sessions       |            |     [x]     |    [x]    |
|        Files With SUID or SGID       |            |     [x]     |    [x]    |
| File Permissions for Sensitive Files |     [x]    |     [x]     |    [x]    |
|    Check for Hashes in Passwd File   |            |     [x]     |    [x]    |
|               Path Info              |     [x]    |     [x]     |    [x]    |
|             Hidden Files             |            |     [x]     |    [x]    |
|               Log Files              |            |     [x]     |    [x]    |
|            Writeable Files           |            |     [x]     |    [x]    |
|        Recently Modified Files       |            |             |    [x]    |
|      Files Containing Passwords      |            |             |    [x]    |
|        Files With Unusual ACL        |            |             |    [x]    |
