import sqlite3

conn = sqlite3.connect('user.db')
cursor = conn.cursor()
cursor.execute("delete from users")
conn.commit()
conn.close()
