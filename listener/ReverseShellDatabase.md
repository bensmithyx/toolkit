<span style="font-family: Baskerville Old Face; font-size: 1em;">
# Reverse Shell Database Ideas:

## How it works
Our program will take an IP Address and Port and will run similar to the pull exploits script where it will take payloads from a website: <https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#bash-udp>
which can normally be run to connect to it. The victim will run a payload given from the website and a listener will be run on the users machine which, in effect, should receive the connection from the payload and allow the user to run shell code as a user. The next step after this would be to upgrade the shell potentially using the shell upgrade tool included in our toolkit to stabilise the shell and then the next step would be to get a higher privilege level and this could be done using our other tool - pullexploits.

## How we can go about it:
- What we could do here is make a text file which contains all the reverse shell commands 
- In C or Python write a piece of code which can be linked onto the main code program which will allow the user to enter in their IP address and port then it will instruct the user to open a listener on their pc at the same port then it will try to execute the payload.
- We could also follow how Ben did it with his pull exploits program as this is a very similar to our tool.

## Ideas:\
- Add the commands to a separate file and read. - OFFLINE  MODE

# Enumeration ideas:

## How it works
https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/tree/master/linPEAS
## How can we go about it:
- Keep it simple to start off with for example, permission checking enumeration first to look for setuid and misconfigured permissions. Then we can add extra enumeration features as seen in linpeas.
