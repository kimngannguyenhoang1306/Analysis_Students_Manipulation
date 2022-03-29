import os
import re
import threading
import json
import csv
from datetime import datetime
from subprocess import Popen, PIPE

# Folder Path
path = "/home/kimngan/Desktop/Analysis_Students_Manipulation/output"

if not os.path.exists(path):
	os.mkdir(path)

	
print('Choose: 1: Clean history cache and set \n\t DateTime 2: Get Log')
choose = input()

if choose == '1':
	args = ["ansible-playbook", "-b", "-v", "Set_DateTime.yml", "--extra-var", "\"crunchify-group\"", "-i", "crunchify-hosts"]
	Set_DateTime = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output = Set_DateTime.communicate()
	print(output)

if choose == '2':
	args = ["ansible-playbook", "-b", "-v", "Check_History.yml", "--extra-var", "\"crunchify-group\"", "-i", "crunchify-hosts"]         
	Check_History = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output = Check_History.communicate()
	print(output)
	
	# Change the directory
	#os.chdir(path)

	# data rows of csv file
	time = ""
	rows = []
	user = ""
	
	# field name
	fields = ['User', 'Time', 'Working Directory', 'Command', 'Duration']
	Sum = []
	file_path = os.getcwd()

	# iterate through all file
	for file in os.listdir(path):
	# Check whether file is in text format or not
		if file.endswith(".txt"):
			file_path = f"{path}/{file}"
			user = file.split('.txt')[0]

			# call read text file function
			f = open(file_path, 'r')
			data = json.loads(f.read())
			
			dt_object = datetime.fromtimestamp(int(data[0].split(" - ")[0]))
			sumDuration = dt_object - dt_object # sum of duration
			
			for item in data:
				line = item.split(" - ")
				time = line[0]
				timestamp = int(time)
				new_dt_object = datetime.fromtimestamp(timestamp)
				duration = new_dt_object - dt_object
				sumDuration += duration
				dt_object = new_dt_object
				line[0] = dt_object
				line.append(duration)
			
				line.insert(0, user)
				rows.append(line)
			
			with open(f'{path}/Statistical_Table.csv', 'w') as f:

				# using csv.writer method from CSV package
				write = csv.writer(f)

				write.writerow(fields)
				write.writerows(rows)

