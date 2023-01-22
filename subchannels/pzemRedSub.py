
import configparser as _cp

import redis

from core.redSubChannel import redSubChannel
from psql.dbOps import dbOps


INI_SEC_NAME = "PZEM"

class pzemRedSub(redSubChannel):

   def __init__(self, ini: _cp.ConfigParser, dbops: dbOps, red: redis.Redis):
      super().__init__(ini=ini, db=dbops, red=red)
      self.sec_ini = self.ini[INI_SEC_NAME]

   def init(self):
      self.sub_channel = self.sec_ini["REDIS_SUB_CHNL"]

   def on_msg(self,  msg: {}):
      print(msg)
