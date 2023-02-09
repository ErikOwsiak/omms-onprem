
import threading, time
import redis, configparser as _cp
from psycopg2.extensions import connection as _psql_conn
# -- --
from lib.utils import utils
from psql.dbOps import dbOps
from psql.dbConnServer import dbConnServer
from core.redSubChannel import redSubChannel
from redchannels.backendReportRedSub import backendReportRedSub


class backendOps(object):

   PROC_NAME = "omms-backend"

   def __init__(self, INI: _cp.ConfigParser
         , red: redis.Redis
         , psqlConn: _psql_conn = None
         , psqlConnStr: str = None):
      # -- -- -- --
      self.ini: _cp.ConfigParser = INI
      self.red: redis.Redis = red
      self.psql_conn: _psql_conn = psqlConn
      self.conn_str: str = psqlConnStr
      self.dbops = dbOps(self.conn_str)
      self.main_thread: threading.Thread = None
      self.pubsub = self.red.pubsub()
      self.reportSub: backendReportRedSub = None
      self.subs: [redSubChannel] = []

   def init(self):
      if self.psql_conn is None and self.psql_conn is not None:
         self.psql_conn = dbConnServer.getConnection(self.conn_str)
      else:
         pass
      # -- -- -- --
      self.reportSub = backendReportRedSub(ini=self.ini, dbops=None
         , dbConnStr=self.conn_str, red=self.red)

   def run_main_thread(self):
      self.main_thread = threading.Thread(target=self.__main_thread)
      self.main_thread.start()

   def __redis_subscribe(self):
      # -- add subs --
      self.subs.append(self.reportSub)
      # -- -- -- --
      for red_sub in self.subs:
         red_sub: redSubChannel = red_sub
         red_sub.init()
         self.pubsub.psubscribe(**{red_sub.chnl_pattern: red_sub.on_msg})
      # -- -- -- --
      self.pubsub_thread: threading.Thread = self.pubsub.run_in_thread(sleep_time=0.001)
      self.pubsub_thread.name = "RedSubThread"
      print(self.pubsub_thread)

   def __main_thread(self):
      self.__redis_subscribe()
      while True:
         if self.__main_loop_tick() != 0:
            time.sleep(4.0)
         else:
            continue

   def __main_loop_tick(self) -> int:
      try:
         time.sleep(2.0)
         return 0
      except Exception as e:
         print(e)
         return 1
