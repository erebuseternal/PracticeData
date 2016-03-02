import os

count = 0
for f in os.listdir('/home/ec2-user/PracticeData/marvel/solrdata'):
	count += 1

print(count)
