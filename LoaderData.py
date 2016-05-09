import os
import informixdb

class DataLoaderTool(object):

  def __init__(self):
    self.Database=os.getenv('DB_CONFIGURE_DB')
    self.Server=os.getenv('INFORMIXSERVER')
    self.Username=os.getenv('DB_CONFIGURE_USERNAME')
    self.Password=os.getenv('DB_CONFIGURE_PASSWORD')
    self.weather_station_data_file = '/home/opuser/sample/data/weather_station.sql'
    self.temperature_monitor_data_file = '/home/opuser/sample/data/temperature_monitor.sql'

  def resetDB(self):
    self.clearDB()
    self.initDB()

  def initDB(self):
    self.weather_station()
    self.temperature_monitor()

  def weather_station(self):
    self.load_data(self.weather_station_data_file)

  def temperature_monitor(self):
    self.load_data(self.temperature_monitor_data_file)

  def load_data(self, data_file):
    try:
        conn = None
        conn = self.connct_ifx()

        count = 0
        for line in open(data_file):
            count += 1
            self.execute_sql(line, conn)

        print 'successfully inserted %d rows' % count
        
    finally:
        if conn:
            conn.close()

  def clearDB(self):
    try:
        conn = None
        conn = self.connct_ifx()
        
        drop_weather_station = "drop table if exists weather_station;"
        drop_temperature_monitor = "drop table if exists temperature_monitor;"

        self.execute_sql(drop_weather_station, conn)
        self.execute_sql(drop_temperature_monitor, conn)
        
        print 'successfully cleared DB'
        
        
    finally:
        if conn:
            conn.close()

  def connct_ifx(self):
    try:
        conn = None
        conn = informixdb.connect(self.Database+'@'+self.Server,self.Username,self.Password)
        if not conn:
            raise Exception("Failed to connect via SQL to " + self.Database+'@'+self.Server,self.Username,self.Password)
        else:
            print("connect !!!!")
            return conn
    except:
        pass
        
  def execute_sql(self, sql, conn):
    try:
        cur = None
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        
        print 'execute',sql,'successfully!!'
        
    finally:
        if cur:
            cur.close()
