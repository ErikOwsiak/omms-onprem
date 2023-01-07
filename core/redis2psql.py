
import redis, setproctitle, psycopg2
from psycopg2.extensions import connection as _conn
from lib.utils import utils
from psql.dbOps import dbOps
from core.logProxy import logProxy


NULL = "null"
SUB_CHANNEL_ROOF = "CK_ROOF_PZEM6_READS"
SUB_CHANNEL_P16_MQTT = "CK_P16_MQTT_READS"


class redis2psql(object):

   def __init__(self, red: redis.Redis, psqlConn: _conn):
      self.prc_name = "redis2psql"
      self.red: redis.Redis = red
      self.psql_conn: _conn = psqlConn
      self.dbops = dbOps(self.psql_conn)
      self.syspath_dbids: {} = {}
      self.pubsub = self.red.pubsub()
      self.pubsub_thread = None
      self.__redis_subscribe()

   # def test_red(self) -> redis.Redis:
   #    try:
   #       ping_val: bool = self.red.ping()
   #       if not ping_val:
   #          raise Exception("RedisPingError!")
   #       # -- -- run -- --
   #       return red
   #    except Exception as e:
   #       logProxy.log_exp(e)

   def __attach_eventers(self):
      pass

   def run(self):
      setproctitle.setproctitle(self.prc_name)
      while True:
         self.__main_loop()

   def __main_loop(self):
      pass

   def __redis_subscribe(self):
      self.pubsub.psubscribe(**{SUB_CHANNEL_ROOF: self.__on_roof_pzem})
      self.pubsub.psubscribe(**{SUB_CHANNEL_P16_MQTT: self.__on_mqtt_p16})
      self.pubsub_thread = self.pubsub.run_in_thread(sleep_time=0.001)

   """
      {'type': 'pmessage', 'pattern': b'CK_PZEM_READER_ROOF'
         , 'channel': b'CK_PZEM_READER_ROOF', 'data': b'#RPT|MODE:Sleep!'}
   """
   def __on_roof_pzem(self, msg: {}):
      if msg["type"] != "pmessage":
         print(f"BadMsg: {msg}")
      # -- do --
      if msg["channel"].decode("utf-8") != SUB_CHANNEL_ROOF:
         return
      # -- do --
      data: str = msg["data"].decode("utf-8")
      if ("#RPT" not in data) and ("PZEM:SS_" not in data) and (not data.endswith("!")):
         print(data)
         return
      # -- do --
      tokens: [] = data[1:-1].split("|")
      if tokens[0] == "RPT":
         self.__proc_pzm_rpt(tokens)
      else:
         pass

   def __on_mqtt_p16(self, msg: {}):
      # -- -- -- -- -- --
      if msg["type"] != "pmessage":
         print(f"BadMsg: {msg}")
      # -- do --
      if msg["channel"].decode("utf-8") != SUB_CHANNEL_P16_MQTT:
         return
      # -- -- -- -- -- --
      data: str = msg["data"].decode("utf-8")
      if ("#RPT" not in data) and ("METER_TAG:ZAMEL_MEW1_" not in data) and (not data.endswith("!")):
         print(data)
         return
      # -- do --
      tokens: [] = data[1:-1].split("|")
      if tokens[0] == "RPT":
         self.__proc_zamel_rpt(tokens)
      else:
         pass

   def __proc_pzm_rpt(self, arr: []):
      try:
         d: {} = utils.arr_dict(arr[1:], ":")
         syspath = d["PATH"]
         if syspath not in self.syspath_dbids.keys():
            dbid: int = self.dbops.get_meter_syspath_dbid(syspath)
            self.syspath_dbids[syspath] = dbid
         # -- do --
         tkwh = d["kWh"]
         dbid = self.syspath_dbids[syspath]
         ins_rval: bool = self.dbops.insert_elect_kwhrs(dbid, tkwh, NULL, NULL, NULL)
         if ins_rval:
            print(f"inserted::[ dbid: {dbid} | t: {tkwh} | l1: ? | l2: ? | l3: ? ]")
         else:
            pass
      except Exception as e:
         logProxy.log_exp(e)

   def __proc_zamel_rpt(self, arr: []):
      try:
         d: {} = utils.arr_dict(arr[1:], ":")
         syspath = d["PATH"]
         if syspath not in self.syspath_dbids.keys():
            dbid: int = self.dbops.get_meter_syspath_dbid(syspath)
            self.syspath_dbids[syspath] = dbid
         # -- do --
         tkwh = d["TkWh"]
         l1kwh = d["L1kWh"]
         l2kwh = d["L2kWh"]
         l3kwh = d["L3kWh"]
         dbid = self.syspath_dbids[syspath]
         ins_rval: bool = self.dbops.insert_elect_kwhrs(dbid, tkwh, l1kwh, l2kwh, l3kwh)
         if ins_rval:
            print(f"inserted::[ dbid: {dbid} | t: {tkwh} | l1: {l1kwh} | l2: {l2kwh} | l3: {l3kwh} ]")
         else:
            pass
      except Exception as e:
         logProxy.log_exp(e)
