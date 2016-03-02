import os
import json

root = '/home/ec2-user/PracticeData/marvel/solrdata'
for filename in os.listdir(root):
	file = open(root + '/' + filename, 'r')
	text = file.read()
	print(text)
	try:
		data = json.loads(text)
	except:
		os.remove(root + '/' + filename)
		continue
	if 'add' in data:
		data = data['add']['doc']
		file = open(root + '/' + filename, 'w')
		text = json.dumps(data, sort_keys=True, indent=4)
		file.write(text)  
