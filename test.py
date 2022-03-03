import json
import csv
import re
from datetime import datetime
from subprocess import Popen, PIPE
import os

args = ["ansible-playbook", "-b", "-v", "crunchify_execute_command.yml", "--extra-var", "\"crunchify-group\"", "-i", "crunchify-hosts"]

test = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

output = test.communicate()[0]

# Folder Path
path = "/home/kimngan/Analysis_Students_Manipulation/output"

# Change the directory
os.chdir(path)

# Read text File

time = ""
rows = []

# iterate through all file
for file in os.listdir():
# Check whether file is in text format or not
	if file.endswith(".txt"):
		file_path = f"{path}/{file}"

	# call read text file function
	f = open(file_path, 'r')
	data = json.loads(f.read())
	print(data)

	# field names
	fields = ['Time', 'Command']
	
	# data rows of csv file
	
	dt_object = None
	for command in data:
		if re.search("^#", command):
			time = command.strip('#')
			timestamp = int(time)
			dt_object = datetime.fromtimestamp(timestamp)
			continue
		rows.append([dt_object, command])


with open('test.csv', 'w') as f:

	# using csv.writer method from CSV package
	write = csv.writer(f)

	write.writerow(fields)
	write.writerows(rows)
