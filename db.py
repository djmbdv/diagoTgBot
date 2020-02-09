import sqlite3

def createTable():
	conn = sqlite3.connect('contacts2.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS users
             (id text, username text, first_name text, last_name text, phone text, status numeric)''')
	c.execute('''CREATE TABLE IF NOT EXISTS groups (name text)''')
	conn.commit()
	conn.close()

def addGroup(group):
	conn = sqlite3.connect('contacts2.db')
	c = conn.cursor()
	add = (group,)
	c.execute("INSERT INTO groups VALUES (?)", add)
	conn.commit()
	conn.close()

def listGroups():
	conn = sqlite3.connect('contacts2.db')
	c = conn.cursor()	
	groups = c.execute("SELECT * FROM groups").fetchall()
	conn.commit()
	conn.close()
	return groups

def insertMany(rows):
	conn = sqlite3.connect('contacts2.db')
	c = conn.cursor()	
	c.executemany("INSERT INTO users VALUES (?,?,?,?,?,?)", rows)
	conn.commit()
	conn.close()

def insertGroup(rows):
	conn = sqlite3.connect('contacts2.db')
	c = conn.cursor()
	for row in rows:
		id = (row[0],)		
		if len(c.execute("SELECT id FROM users WHERE id = ?", id).fetchall()) == 0:
			c.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", row)

	conn.commit()
	conn.close()

def changeStatus(id):
	conn = sqlite3.connect('contacts2.db')
	c = conn.cursor()
	c.execute("UPDATE users SET status = 1 WHERE id=?", id)
	conn.commit()
	conn.close()

def changeStatusError(id):
	conn = sqlite3.connect('contacts2.db')
	c = conn.cursor()
	c.execute("UPDATE users SET status = -1 WHERE id=?", id)
	conn.commit()
	conn.close()
def selectSome(qtt):
	result = []
	conn = sqlite3.connect('contacts2.db')
	c = conn.cursor()
	result = c.execute("SELECT id,username FROM users WHERE status = 0").fetchall()
	return result[0:qtt]

def stats(s):
	conn = sqlite3.connect('contacts2.db')
	c = conn.cursor()
	if s == 0:
		return c.execute("SELECT COUNT(id) FROM users").fetchone()
	if s == 1:
		return c.execute("SELECT COUNT(id) FROM users WHERE status = 1").fetchone()
	if s == 2:
		return c.execute("SELECT COUNT(id) FROM users WHERE status = 0").fetchone()
	