import informixdb
import os

def execute_sql_file(sql_file):
	try:
		print(Database,Server,Username,Password)
		cur = conn = None
		conn = informixdb.connect(Database+'@'+Server,Username,Password)
		if not conn:
			raise Exception("Failed to connect via SQL to " + dbservername)
			return
		cur = conn.cursor()
 		count = 0
		for(line in sql_file):
			cur.execute(line)
			count++
		print(count + 'line(s) executed')
		conn.commit()
	
	finally:
	if cur:
		cur.close()
	if conn:
		conn.close()
