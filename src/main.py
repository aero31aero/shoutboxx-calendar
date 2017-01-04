#! /usr/bin/env python3
import post
import os
from datetime import datetime
def run():
	apitoken = os.environ['FACEPY_TOKEN']
	groupid = '300189226756572'
	timelimit = datetime.strptime("2015-02-06", '%Y-%m-%d')
	facebook = post.FacebookHandler(apitoken,groupid)
	allposts = facebook.scrape(timelimit)
	print(len(allposts))
run()