import informixdb
import os

def get_cmd_line(sql_file):
	try:
		str = open(sql_file).read()
		str = str.replace('\t','').replace('\n','')
		strlist = str.split(';')
		
	finally:
		if strlist:
			return strlist
		else:
			print('error')


def execute_sql_file(sql_file, conn):
	try:
		print(Database,Server,Username,Password)
		if not conn:
			raise Exception("Failed to connect via SQL to " + dbservername)
			return
		cur = conn.cursor()
 		count = 0
 		strlist = get_cmd_line(sql_file)
		for line in strlist:
			cur.execute(line)
			count=count+1
		print(count + 'line(s) executed')
		conn.commit()
	
	finally:
		if cur:
			cur.close()
		if conn:
			conn.close()
