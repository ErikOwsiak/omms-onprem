
import configparser as _cp, redis
import threading, typing as t
# -- core --
from core.datatypes import redSubMsg
from core.redSubChannel import redSubChannel
from psql.dbOps import dbOps
from lib.utils import utils
from core.logProxy import logProxy
# -- reports --
from core.reports.reportEngine import reportEngine
from core.reports.metCircConsumption import metCircConsumption
from core.reports.clientMonthly import clientMonthly
from core.reports.xlsOut import xlsOut


INI_SEC_NAME = "BACKEND"


class systemErrorsRedSub(redSubChannel):

   def __init__(self, ini: _cp.ConfigParser
         , dbops: [dbOps, None]
         , dbConnStr: str
         , red: redis.Redis):
      super().__init__(ini=ini, db=dbops, red=red)
      # -- -- -- --
      self.conn_str: str = dbConnStr
      self.sec_ini = self.ini[INI_SEC_NAME]

   def init(self):
      self.chnl_pattern = self.sec_ini["ERROR_PUBLISH_CHNL"]

   def on_msg(self,  msg: {}):
      redmsg: redSubMsg = redSubMsg(msg)
      # -- -- -- --
      if redmsg.patt != self.chnl_pattern:
         print(f"BadPattern: {self.chnl_pattern}")
         return
      # -- -- -- --
      print(f"\n[ CHNL_PATT: {redmsg.patt} | CHNL: {redmsg.channel} ]\n")
      print(f"ErrorMsg:\n\t{redmsg.data}")
