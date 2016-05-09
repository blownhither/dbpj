#!/bin/python
import informixdb
import os

Database = 'd_1460371357365469'
#Server='172.16.13.186'
Server='ifxserver1'
Username = 'tqbodnho'
Password = 'JSe2lR1cH6'

def test_SQL():

    try:
        cur = conn = None
        #connect
        conn = informixdb.connect(Database+'@'+Server,Username,Password)
        if not conn:
            raise Exception("Failed to connect via SQL to " + dbservername)
        else:
            print("connect !!!!")
        #get cursor
        cur = conn.cursor()
        #query count of testtable(if not exists,created)
        cur.execute("create table if not exists testtable(id int, str char(50))")
        cur.execute("select count(*) from testtable")
        a = cur.fetchall()
        print("Count is :")
        print(a[0][0])

        #insert a record into testtable
        cur.execute("insert into testtable values(1,'hello')")
        print("inserted a record!")

        #query count of testtable again
        cur.execute("select count(*) from testtable")
        a = cur.fetchall()
        print("Count is :")
        print(a[0][0])

        #commit
        conn.commit()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

#main()

if __name__=='__main__':
    print("-----------------------------------------this is a SQL test")
    test_SQL()
    print("-----------------------------------------this is a SQL test")

