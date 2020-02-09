import sqlite3
import db

conn = sqlite3.connect('contacts.db')

c = conn.cursor()

# # Create table
# c.execute('''CREATE TABLE IF NOT EXISTS users
#              (id text, username text, first_name text, last_name text, phone text, status numeric)''')

# Insert a row of data
# c.execute("INSERT INTO users VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
# c.execute("INSERT INTO users VALUES ('856854', 'antuan', 'jesus', 'sfsfd', 'su telefono', 0)")

# Save (commit) the changes
# conn.commit()
# id=('324',)
# c.execute("SELECT * FROM users WHERE id=?", id)
# r = c.fetchall()

# print(len(r))

print(c.execute("SELECT COUNT(id) FROM users").fetchall())
# print(len(c.execute("SELECT id FROM users WHERE id = '1'").fetchall()))
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
