import os
import informixdb

class DBTool(object):

	def __init__(self):
		self.Database=os.getenv('DB_CONFIGURE_DB')
		self.Server=os.getenv('INFORMIXSERVER')
		self.Username=os.getenv('DB_CONFIGURE_USERNAME')
		self.Password=os.getenv('DB_CONFIGURE_PASSWORD')
	
	def execute_sql(self, sql, conn):
		try:
			cur = None
			cur = conn.cursor()
			cur.execute(sql)
			conn.commit()
			print('execute'+sql+'successfully!!')
		finally:
			if cur:
				cur.close()

