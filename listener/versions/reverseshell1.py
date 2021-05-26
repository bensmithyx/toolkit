import requests
r = requests.get("https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md")
#print(r.content)
print(r.text)
text = r.text
for i in range (50):
    if "#include" in text.split("```")[i]:
        print(text.split("```")[i],"\n\n\n\n")
    elif "#" in text.split("```")[i] or "powershell" in text.split("```")[i]:
        None
    else:
        print(text.split("```")[i],"\n\n\n\n")
