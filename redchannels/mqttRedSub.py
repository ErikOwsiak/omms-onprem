
import configparser as _cp, redis
from core.redSubChannel import redSubChannel
from core.datatypes import redSubMsg
from psql.dbOps import dbOps
from lib.utils import utils


INI_SEC_NAME = "MQTT"
RPT_PWRS = "#RPT:POWERSTATS"
RPT_KWHR = "#RPT:KWHRS"


class mqttRedSub(redSubChannel):

   def __init__(self, ini: _cp.ConfigParser, dbops: dbOps, red: redis.Redis):
      super().__init__(ini=ini, db=dbops, red=red)
      self.sec_ini = self.ini[INI_SEC_NAME]

   def init(self):
      self.chnl_pattern = self.sec_ini["REDIS_SUB_CHNL_PATT"]

   def on_msg(self,  msg: {}):
      redmsg: redSubMsg = redSubMsg(msg)
      # -- -- do -- --
      if redmsg.patt != self.chnl_pattern:
         print(f"BadPattern: {self.chnl_pattern}")
         return
      # -- -- do -- --
      if redmsg.data[0] != "(" or redmsg.data[-1] != ")":
         print("BadDataWrapper")
         return
      # -- test string for some more tokens --
      if ("#RPT:" not in redmsg.data) and ("ModbusAddr:" not in redmsg.data):
         print(redmsg.data)
         return
      # -- -- feedback info -- --
      print(f"\n[ CHNL_PATT: {redmsg.patt} | CHNL: {redmsg.channel} ]\n")
      # -- -- do: strip () from start & end -- --
      tokens: [] = redmsg.data[1:-1].split("|")
      if tokens[0].upper() == RPT_PWRS:
         self.__save_power_stats_v1(arr=tokens)
      elif tokens[0].upper() == RPT_KWHR:
         self.__save_kwhrs_v1(arr=tokens)
      else:
         print(f"BadTokens: {tokens[0]}, {tokens[1]}")
      # -- -- do -- --

   def __save_power_stats_v1(self, arr: []):
      try:
         _dict: {} = utils.arr_dict(arr, ":")
         syspath: str = _dict["PATH"]
         meter_rowid, _ = self.dbops.get_met_circ_info(syspath)
         self.dbops.insert_elect_pwr_stats(meter_rowid, _dict)
      except Exception as e:
         print(e)

   def __save_kwhrs_v1(self, arr: []):
      _dict: {} = utils.arr_dict(arr, ":")
      syspath: str = _dict["PATH"]
      meter_rowid, _ = self.dbops.get_met_circ_info(syspath)
      self.dbops.insert_elect_kwhrs_dict(meter_rowid, _dict)
