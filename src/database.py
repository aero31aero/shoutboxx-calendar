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
				post_id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
				fb_post_id VARCHAR(200) DEFAULT NULL,
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
