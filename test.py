import json
import csv
import re
from datetime import datetime, date
from subprocess import Popen, PIPE
import os
import threading

# Folder Path
path = "/home/kimngan/Analysis_Students_Manipulation/output"

if not os.path.exists(path):
	os.mkdir(path)

	
print('Choose: 1: SetTime 2: GetLog')
choose = input()

if choose == '1':
	args = ["ansible-playbook", "-b", "-v", "SetTime.yml", "--extra-var", "\"crunchify-group\"", "-i", "crunchify-hosts"]
	test = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output = test.communicate()[1]

if choose == '2':
	'''args1 = ["ansible-playbook", "-b", "-v", "crunchify_execute_command.yml", "--extra-var", "\"crunchify-group\"", "-i", "crunchify-hosts"]         
	test1 = Popen(args1, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output1 = test1.communicate()[1]
	print(output1)'''

	time = ""
	rows = []
	user = ""
	fields = []
	file_path = os.getcwd()
	# field names
	fields = ['User', 'Time', 'Command', 'Duration']
	
	
	# iterate through all file
	for file in os.listdir(path):
	# Check whether file is in text format or not
		if file.endswith(".txt"):
			file_path = f"{path}/{file}"
			user = file.split('.txt')[0]

			# call read text file function
			f = open(file_path, 'r')
			data = json.loads(f.read())
			
			dt_object = datetime.fromtimestamp(int(data[0].strip('#')))
			totalDuration = dt_object - dt_object
			
			# data rows of csv file	
			for command in data:
				if re.search("^#", command):
					time = command.strip('#')
					timestamp = int(time)
					new_dt_object = datetime.fromtimestamp(timestamp)
					duration = new_dt_object - dt_object
					totalDuration += duration
					print(totalDuration)
					dt_object = new_dt_object
					continue
				rows.append([user, dt_object, command, duration])


	with open(f'{path}/test.csv', 'w') as f:

		# using csv.writer method from CSV package
		write = csv.writer(f)

		write.writerow(fields)
		write.writerows(rows)

