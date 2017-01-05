import pymysql
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
				event_id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
				google_event_id VARCHAR(200) DEFAULT NULL,
				title VARCHAR(200) DEFAULT NULL,
				description VARCHAR(5000) DEFAULT NULL,
				event_date DATETIME DEFAULT NULL,
				event_venue VARCHAR(200) DEFAULT NULL,
				photo_url VARCHAR(500) DEFAULT NULL,
				organiser VARCHAR(200) DEFAULT NULL,
				link_to_post VARCHAR(200) DEFAULT NULL,
				event_uploaded BOOLEAN DEFAULT FALSE
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
