#!/bin/python
import informixdb
import os

Database = 'd_1460371357365469'
#Server='172.16.13.186'
Server='ifxserver1'
Username = 'tqbodnho'
Password = 'JSe2lR1cH6'

cur = conn = None
conn = informixdb.connect(Database+'@'+Server,Username,Password)
if not conn:
	raise Exception("Failed to connect via SQL to " + dbservername)
else:
	print("connected to database!\nuse "+__name__+".conn.cursor()")
