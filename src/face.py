from facepy import GraphAPI
import facepy
import os
graph = GraphAPI(os.environ['FACEPY_TOKEN']);
# print os.environ['FACEPY_TOKEN']

groupid='300189226756572'
posts = graph.get(groupid+'/feed', limit=10)
for post in posts['data']:
	print post['from']