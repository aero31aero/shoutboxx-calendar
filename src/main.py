#! /usr/bin/env python3
import post
import database

import os
def run():
	apitoken = os.environ['FACEPY_TOKEN']
	groupid = '300189226756572'
	db = database.DatabaseHandler("localhost","root","root","sbxcal")
	db.setupDatabase()
	facebook = post.FacebookHandler(apitoken,groupid)
	allposts = facebook.scrape(db.getLatestPostTime())
	print(len(allposts))
	for eachpost in allposts:
		try:
			db.insertPost(eachpost)
		except KeyError as e:
			print(type(e))
			print(e)
run()