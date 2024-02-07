import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Creating the table
c.execute('''CREATE TABLE users
	(username text, password text, email text)''')

# Saving the changes
conn.commit()

# Closing the connection
conn.close()
