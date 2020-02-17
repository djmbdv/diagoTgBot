import sqlite3

class Database:
	def __init__(self, database_file):
		self.file_name = database_file
	def createTable(self):
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()
		c.execute('''CREATE TABLE IF NOT EXISTS users
				(id text, username text, first_name text, last_name text, phone text, status numeric)''')
		c.execute('''CREATE TABLE IF NOT EXISTS channels (name UNIQUE)''')
		self.conn.commit()

	def addGroup(self,group):
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()
		add = (group,)
		try:
			c.execute("INSERT INTO channels VALUES (?)", add)
		except:
			pass
		self.conn.commit()
	def addGroups(self,groups):
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()
		for group in  groups:
			add = (group,)
			try:
				c.execute("INSERT INTO channels VALUES (?)", add)
			except:
				pass
		self.conn.commit()
	def close(self):
		self.conn.close()
	def listGroups(self):
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()	
		groups = c.execute("SELECT * FROM channels").fetchall()
		self.conn.commit()
		return groups

	def insertMany(self,rows):
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()
		try:
			c.executemany("INSERT INTO users VALUES (?,?,?,?,?,?)", rows)
		except:
			pass
		self.conn.commit()

	def insertGroup(self,rows):
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()
		for row in rows:
			id = (row[0],)		
			try:
				c.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", row)
			except:
				pass
		self.conn.commit()

	def changeStatus(self,id):
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()
		c.execute("UPDATE users SET status = 1 WHERE id=?", id)
		self.conn.commit()

	def changeStatusError(self,id):
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()
		c.execute("UPDATE users SET status = -1 WHERE id=?", id)
		self.conn.commit()
	def selectSome(self,qtt):
		result = []
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()
		result = c.execute("SELECT id,username FROM users WHERE status = 0").fetchall()
		return result[0:qtt]

	def stats(self,s):
		self.conn = sqlite3.connect(self.file_name)
		c = self.conn.cursor()
		if s == 0:
			return c.execute("SELECT COUNT(id) FROM users").fetchone()
		if s == 1:
			return c.execute("SELECT COUNT(id) FROM users WHERE status = 1").fetchone()
		if s == 2:
			return c.execute("SELECT COUNT(id) FROM users WHERE status = 0").fetchone()
		if s == 3:
			return c.execute("SELECT COUNT(name) FROM channels").fetchone()
		