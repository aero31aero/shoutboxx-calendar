#! /usr/bin/env python3
import post
import database

import os
from datetime import datetime
def run():
	apitoken = os.environ['FACEPY_TOKEN']
	groupid = '300189226756572'
	timelimit = datetime.strptime("2014-12-15", '%Y-%m-%d')
	facebook = post.FacebookHandler(apitoken,groupid)
	allposts = facebook.scrape(timelimit)
	print(len(allposts))
	db = database.DatabaseHandler("localhost","root","root","sbxcal")
	db.setupDatabase()
	for eachpost in allposts:
		try:
			db.insertPost(eachpost)
		except KeyError as e:
			print(type(e))
			print(e)
run()