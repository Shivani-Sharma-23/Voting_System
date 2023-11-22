import sqlite3
import sys

con = lite.connect('finger.db')
cursor = connection.cursor()
newname = "Xujia Ji"

with con:
	cur = con.cursor()
	cur.execute("CREATE TABLE FINGER(ID INT, Name TEXT)")
	cur.execute("INSERT INTO FINGER VALUES(newname)"
con.close()
