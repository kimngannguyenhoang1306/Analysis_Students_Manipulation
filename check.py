"""import pandas as pd

df = pd.read_csv("output/test.csv")

# Commands from user
check = df.groupby('User')
for User,group in check:
	print(User)
	print(group["Command"].tolist())"""

check1 = ["echo", "file dolls.jpg", 
"binwalk -e dolls.jpg",
"cd _dolls.jpg.extracted/",
"cd base_images/",
"binwalk -e 2_c.jpg", 
"cd _2_c.jpg.extracted/",
"cd base_images/",
"binwalk -e 3_c.jpg", 
"binwalk -e chall",
"cd _3_c.jpg.extracted/",
"cd base_images/",
"binwalk -e 4_c.jpg", 
"cd _4_c.jpg.extracted/",
"cat flag.txt",
"strings 5F0040.jffs2"]

"""binwalk -e chall
c1:
strings _chall.extracted/* | grep CTF (strings _chall.extracted/*|grep CTF cũng sẽ đúng)
c2:
strings * | grep CTF
c3:
strings 5F0040.jffs2 | grep CTF (strings 5F0040.jffs2)"""

'''check1 = ["cd ..", "binwalk -e chal", "strings 5F0040.jffs2 | grep CTF", ]'''
# default solution	
keywords = ["file", "binwalk", "foremost", "cd", "cat", "strings"]

script1 = {
	"fileNames": ["dolls.jpg", "2_c.jpg", "3_c.jpg", "4_c.jpg", "flag.txt", "base_images"],
	"modelCmds": ["binwalk -e dolls.jpg", "binwalk -e 2_c.jpg", "binwalk -e 3_c.jpg", "binwalk -e 4_c.jpg", "cat flag.txt"],
	"currentModelCmd": -1,
	"currentCheckCmd": -1
}

script2 = {
	"fileNames": ["chall", "_chall.extracted", "*", "5F0040.jffs2"],
	"modelCmds": ["binwalk -e chall", {"main": ["strings _chall.extracted/*", "strings *", "strings 5F0040.jffs2"], "option1": ["grep CTF"]}],
	"currentModelCmd": -1,
	"currentCheckCmd": -1
}

scripts = {
	"script1": script1,
	"script2": script2
}

def Check_User_Valid_Cmd(command):

	valid_cmd = []
	for checkCmd in command:
		if list(set(keywords).intersection(checkCmd.split())):
			valid_cmd.append(checkCmd)
	return valid_cmd
	
'''for i in range(len(user_ip)):
	Check_User_Valid_Cmd(user_command[i])'''	

check = Check_User_Valid_Cmd(check1)

scriptsValues = list(scripts.values())

currentScript = 0
def findCurrentScript(checkCmd):
	global currentScript
	for i in range(len(scriptsValues)):
		for fileName in scriptsValues[currentScript]["fileNames"]:
			if fileName in checkCmd:
				return currentScript
		currentScript = (currentScript + 1) % len(scripts)

for checkCmd in check:
	splittedCheckCmd = [splitCmd.strip() for splitCmd in checkCmd.split("|")]
	mainCheckCmd = splittedCheckCmd[0]
	currentScript = findCurrentScript(mainCheckCmd)
	if currentScript != None:
		modelCmds = scriptsValues[currentScript]["modelCmds"]
		for modelCmd in modelCmds:
			flag = 0
			if (mainCheckCmd == modelCmd):
				if (scriptsValues[currentScript]["currentModelCmd"] + 1 == modelCmds.index(modelCmd)):
					scriptsValues[currentScript]["currentModelCmd"] = modelCmds.index(modelCmd)
					flag = 1
					break
				else:
					flag = 0
					break
			elif isinstance(modelCmd, dict) and mainCheckCmd in modelCmd["main"]:
				if len(splittedCheckCmd) > 1:
					if splittedCheckCmd[1] not in modelCmd["option1"]:
						flag = 0
						break
				if (scriptsValues[currentScript]["currentModelCmd"] + 1 == modelCmds.index(modelCmd)):
					scriptsValues[currentScript]["currentModelCmd"] = modelCmds.index(modelCmd)
					flag = 1
					break
			else:
				flag = 2
		if flag == 0:
			print("warning " + checkCmd)
			#break

for script, value in scripts.items():
	if value["currentModelCmd"] + 1 == len(value["modelCmds"]):
		print(script + " completed")

	
	
	
	
