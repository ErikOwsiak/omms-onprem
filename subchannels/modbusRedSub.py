
import configparser as _cp
from lib.utils import utils
from psql.dbOps import dbOps
from core.redSubChannel import redSubChannel


INI_SEC_NAME = "MODBUS"


class modbusRedSub(redSubChannel):

   def __init__(self, ini: _cp.ConfigParser, dbops: dbOps):
      super().__init__(ini=ini, db=dbops)
      self.sec_ini = self.ini[INI_SEC_NAME]

   def init(self):
      self.sub_channel = self.sec_ini["REDIS_SUB_CHNL"]

   def on_msg(self,  msg: {}):
      # -- -- do -- --
      if msg["type"] != "pmessage":
         print(f"BadMsg: {msg}")
      # -- -- do -- --
      if msg["pattern"].decode("utf-8") != self.sub_channel:
         print(f"BadPattern: {self.sub_channel}")
         return
      # -- -- do -- --
      data: str = msg["data"].decode("utf-8")
      if data[0] != "(" or data[-1] != ")":
         print("BadDataWrapper")
         return
      # -- test string for some more tokens --
      if ("#RPT:" not in data) and ("ModbusAddr:" not in data):
         print(data)
         return
      # -- -- do -- --
      tokens: [] = data[1:-1].split("|")
      if tokens[0] == "#RPT:powerStats":
         self.__save_power_stats(arr=tokens)
      elif tokens[0] == "#RPT:kWhrs":
         self.__save_kwhrs(arr=tokens)
      else:
         print(f"BadTokens: {tokens[0]}, {tokens[1]}")
      # -- -- do -- --

   def __save_power_stats(self, arr: []):
      try:
         _dict: {} = utils.arr_dict(arr, ":")
         syspath: str = _dict["PATH"]
         dbid: int = self.dbops.get_meter_syspath_dbid(syspath)
         self.dbops.insert_elect_pwr_stats(dbid, _dict)
      except Exception as e:
         print(e)

   def __save_kwhrs(self, arr: []):
      _dict: {} = utils.arr_dict(arr, ":")
      syspath: str = _dict["PATH"]
      dbid: int = self.dbops.get_meter_syspath_dbid(syspath)
      self.dbops.insert_elect_kwhrs_dict(dbid, _dict)
