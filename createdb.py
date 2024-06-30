import sqlite3

conn = sqlite3.connect('user.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(username text, password text, firstName text, lastName text, email text)")
conn.commit()
