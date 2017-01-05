from facepy import GraphAPI
import facepy
from datetime import datetime
class FacebookHandler():
	def __init__(self,apitoken,groupid):
		self.graph = GraphAPI(apitoken)
		self.groupid = groupid
		self.apitoken = apitoken
	def scrape(self, timelimit):
		allposts = []
		parameters = "id,updated_time,message,from,object_id&limit=10&icon_size=16"
		url = self.groupid + "/feed?fields=" + parameters + "&access_token=" + self.apitoken
		try:
			getposts = True
			while getposts:
				p = self.graph.get(url)
				url = p['paging']['next'].split('v2.2/')[1]
				p_posts = p['data']
				for post in p_posts:
					postdate = datetime.strptime(post['updated_time'].split('T')[0], '%Y-%m-%d')
					if postdate < timelimit:
						getposts = False
						break
					photo_id = post.get('object_id',None)
					photo_url = None
					if photo_id is not None :
						photo_url_dict = self.graph.get(photo_id,fields="link")
						photo_url = photo_url_dict["link"]
					post['photo_url'] = photo_url
					allposts.append(post)
					print(post['updated_time']+"\t"+post['from']['name'])
		except Exception as e:
			print(e)
		return allposts
