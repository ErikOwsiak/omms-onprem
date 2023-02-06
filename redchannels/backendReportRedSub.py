
import configparser as _cp, redis
import threading
# -- core --
from core.datatypes import redSubMsg
from core.redSubChannel import redSubChannel
from psql.dbOps import dbOps
from lib.utils import utils
from core.logProxy import logProxy
# -- reports --
from core.reports.backFiller import backFiller
from core.reports.circuitMonthly import circuitMonthly
from core.reports.clientMonthly import clientMonthly


INI_SEC_NAME = "BACKEND"


class backendReportRedSub(redSubChannel):

   def __init__(self, ini: _cp.ConfigParser
         , dbops: dbOps
         , red: redis.Redis):
      super().__init__(ini=ini, db=dbops, red=red)
      self.sec_ini = self.ini[INI_SEC_NAME]

   def init(self):
      self.chnl_pattern = self.sec_ini["WEBUI_TO_BACKEND_CHNL"]

   def on_msg(self,  msg: {}):
      redmsg: redSubMsg = redSubMsg(msg)
      # -- -- -- --
      if redmsg.patt != self.chnl_pattern:
         print(f"BadPattern: {self.chnl_pattern}")
         return
      # -- -- -- --
      print(f"\n[ CHNL_PATT: {redmsg.patt} | CHNL: {redmsg.channel} ]\n")
      tag, row_id = [x.strip() for x in redmsg.data.split(":")]
      if tag == "NEW_REPORT_JOB":
         row_id: int = int(row_id)
         report_thread: threading.Thread = \
            threading.Thread(target=self.__report_thread, args=(row_id,))
         report_thread.start()
      else:
         print([tag, row_id])

   def __report_thread(self, rowid: int):
      row: [] = self.dbops.get_report_data(rowid)
      serid, _, dts_issue, args, _, _, _, _ = row
      if rowid != int(serid):
         self.dbops.update_report_data(rowid, -1, "BadRowID")
         return
      arr: [] = args.split(";")
      d = utils.arr_dict(arr, ":")
      self.dbops.update_report_data(rowid, 10, F"GOT_ARGS: {args}\n")
      try:
         backfiller: backFiller = backFiller(self.dbops)
         y: int = int(d["year"])
         m: int = int(d["month"])
         data: ([], []) = backfiller.validate_data_dates(year=y, month=m)
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         pass
