#! /usr/bin/env python3
import post
import database
import event

import os

def run():
	apitoken = os.environ['FACEPY_TOKEN']
	groupid = '300189226756572'
	db = database.DatabaseHandler("localhost","root","root","sbxcal")
	db.setupDatabase()
	evt = event.EventScraper()
	facebook = post.FacebookHandler(apitoken,groupid)
	allposts = facebook.scrape(db.getLatestPostTime())
	print(len(allposts))
	for eachpost in allposts:
		try:
			db.insertPost(eachpost)
			if evt.isEvent(eachpost):
				newevent = evt.getEvent(eachpost)
				db.insertEvent(newevent)
				print(newevent)
		except KeyError as e:
			# swallow the exception
			print(type(e))
			print(e)
			# pass
run()