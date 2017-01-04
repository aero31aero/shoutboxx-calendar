import pymysql
class DatabaseHandler(object):
	"""docstring for DatabaseHandler"""
	def __init__(self, hostname, username, password, databasename):
		super(DatabaseHandler, self).__init__()
		try:
			self.db = pymysql.connect(hostname,username,password,databasename)
			self.cursor = db.cursor()
		except Exception as e:
			print(type(e))
			print(e)
			exit(1)
	# def createdb(self):
