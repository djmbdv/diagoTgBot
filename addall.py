import sqlite3

def createTable():
	conn = sqlite3.connect('channels.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS channels name text)''')	
	conn.commit()
	conn.close()

def insertMany(rows):
	conn = sqlite3.connect('channels.db')
	c = conn.cursor()	
	c.executemany("INSERT INTO channels VALUES (?)", rows)
	conn.commit()
	conn.close()
