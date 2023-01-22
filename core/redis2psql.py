
import threading, time
import redis, configparser as _cp
from psycopg2.extensions import connection as _psql_conn
# -- --
from lib.utils import utils
from psql.dbOps import dbOps
from core.logProxy import logProxy
# -- channels --
from core.redSubChannel import redSubChannel
from subchannels.mqttRedSub import mqttRedSub
from subchannels.modbusRedSub import modbusRedSub
from subchannels.pzemRedSub import pzemRedSub


NULL = "null"


class redis2psql(object):

   PROC_NAME = "redis2psql"

   def __init__(self, INI: _cp.ConfigParser, red: redis.Redis, psqlConn: _psql_conn):
      self.ini: _cp.ConfigParser = INI
      self.red: redis.Redis = red
      self.psql_conn: _psql_conn = psqlConn
      self.dbops = dbOps(self.psql_conn)
      self.syspath_dbids: {} = {}
      self.pubsub_thread: threading.Thread = None
      # -- -- channels -- --
      self.pubsub = self.red.pubsub()
      self.pzemSub: pzemRedSub = \
         pzemRedSub(ini=self.ini, dbops=self.dbops, red=self.red)
      self.mqttSub: mqttRedSub = \
         mqttRedSub(ini=self.ini, dbops=self.dbops, red=self.red)
      self.modbusSub: modbusRedSub = \
         modbusRedSub(ini=self.ini, dbops=self.dbops, red=self.red)
      self.subs: [redSubChannel] = []

   def int(self):
      self.__redis_subscribe()

   def run(self):
      while True:
         self.__main_loop()

   def __main_loop(self):
      if self.pubsub_thread.is_alive():
         print(f"ThreadRunning: {self.pubsub_thread.name}")
      time.sleep(2.0)

   def __redis_subscribe(self):
      # -- add subs --
      self.subs.append(self.mqttSub)
      self.subs.append(self.pzemSub)
      self.subs.append(self.modbusSub)
      # -- -- -- --
      for red_sub in self.subs:
         red_sub: redSubChannel = red_sub
         red_sub.init()
         self.pubsub.psubscribe(**{red_sub.sub_channel: red_sub.on_msg})
      # -- -- -- --
      self.pubsub_thread: threading.Thread = self.pubsub.run_in_thread(sleep_time=0.001)
      self.pubsub_thread.name = "RedSubThread"
      print(self.pubsub_thread)
