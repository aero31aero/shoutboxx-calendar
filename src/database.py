import pymysql
from datetime import datetime
class DatabaseHandler(object):
	"""docstring for DatabaseHandler"""
	def __init__(self, hostname, username, password, databasename):
		super(DatabaseHandler, self).__init__()
		try:
			self.db = pymysql.connect(hostname,username,password,databasename)
			self.cursor = self.db.cursor()
			print("Done.")
		except Exception as e:
			print(type(e))
			print(e)
			exit(1)
	def setupDatabase(self):
		create_table_posts = """
			CREATE TABLE IF NOT EXISTS posts (
				fb_post_id VARCHAR(200) NOT NULL PRIMARY KEY,
				message VARCHAR(5000) DEFAULT NULL,
				upd_time DATETIME DEFAULT NULL,
				photo_url VARCHAR(500) DEFAULT NULL,
				poster_name VARCHAR(200) DEFAULT NULL,
				poster_id VARCHAR(200) DEFAULT NULL,
				event_id int(11)
			);
		"""
		create_table_events = """
			CREATE TABLE IF NOT EXISTS events (
				fb_post_id VARCHAR(500) NOT NULL PRIMARY KEY,
				google_event_id VARCHAR(500) DEFAULT NULL,
				title VARCHAR(500) DEFAULT NULL,
				starttime DATETIME DEFAULT NULL,
				venue VARCHAR(200) DEFAULT NULL,
				uploaded BOOLEAN DEFAULT FALSE
			);
		"""
		try:
			self.cursor.execute(create_table_posts)
			self.cursor.execute(create_table_events)
		except Exception as e:
			print(type(e))
			print(e)
			exit(1)

	def insertPost(self,post):
		print("Inserting/Updating post")
		sql_insert_post = (
			"INSERT INTO posts "
			"(fb_post_id, message, upd_time, photo_url, poster_name, poster_id)"
			"VALUES (%s, %s, %s, %s, %s, %s)"
			)
		post_info = [
			post['id'],
			post['message'],
			post['timestamp'],
			post['photo_url'],
			post['from']['name'],
			post['from']['id']
			]
		try:
			result = self.cursor.execute(sql_insert_post,post_info)
			self.db.commit()
		except pymysql.err.IntegrityError as e:
			print("Duplicate Post. Updating existing post.")
			self.db.rollback()
			sql_delete_post="DELETE FROM posts WHERE fb_post_id=%s;"
			self.cursor.execute(sql_delete_post,post['id'])
			self.cursor.execute(sql_insert_post,post_info)
			self.db.commit()
		except Exception as e:
			print(type(e))
			print(e)
			self.db.rollback()
	def insertEvent(self,event):
		print("Inserting/Updating Event")
		sql_insert_event = (
			"INSERT INTO events "
			"(title, starttime, venue, fb_post_id)"
			"VALUES (%s, %s, %s, %s)"
			)
		event_info = [
			event['title'],
			event['datetime'],
			event['venue'],
			event['id']
			]
		try:
			result = self.cursor.execute(sql_insert_event,event_info)
			self.db.commit()
		except pymysql.err.IntegrityError as e:
			print("Duplicate Event. Updating existing event.")
			self.db.rollback()
			sql_update_event=("UPDATE events "
				"SET title=%s,starttime=%s,venue=%s,uploaded=0 "
				"WHERE fb_post_id=%s;")
			self.cursor.execute(sql_update_event,event)
			self.db.commit()
		except Exception as e:
			print(type(e))
			print(e)
			self.db.rollback()
	def getLatestPostTime(self):
		sql_select_post = "SELECT upd_time FROM posts ORDER BY upd_time DESC LIMIT 1;"
		result = datetime.strptime("2014-12-15", '%Y-%m-%d')
		try:
			self.cursor.execute(sql_select_post)
			data = self.cursor.fetchone()
			if data is not None:
				result = data[0]
		except Exception as e:
			print(type(e))
			print(e)
		print("Timelimit:",result)
		return result
	def getToBeUploadedPosts(self):
		sql_select_event = "SELECT * from events WHERE uploaded=0;"
		# sql_select_event = "SELECT * from posts;"
		results = []
		try:
			self.cursor.execute(sql_select_event)
			data = self.cursor.fetchall()
			if data is not None:
				for row in data:
					results.append(row)
		except Exception as e:
			print(type(e))
			print(e)
		return results
