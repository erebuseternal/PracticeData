import os
import json

root = '/home/ec2-user/PracticeData/marvel/solrdata'
for filename in os.listdir(root):
	file = open(root + '/' + filename, 'r')
	text = file.read()
	data = json.loads(text)
	try:
		f = data['weight']
	except:
		continue
	if type(data['weight']) == unicode:
		del data['weight']
		file = open(root + '/' + filename, 'w')
		text = json.dumps(data, sort_keys=True, indent=4)
		file.write(text)  
