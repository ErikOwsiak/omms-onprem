
import configparser as _cp, redis
import threading, typing as t
# -- core --
from core.datatypes import redSubMsg
from core.redSubChannel import redSubChannel
from psql.dbOps import dbOps
from lib.utils import utils
from core.logProxy import logProxy
# -- reports --
from core.reports.backFiller import backFiller
from core.reports.metCircConsumption import metCircConsumption
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

   def __report_thread(self, report_job_id: int):
      row: [] = self.dbops.get_report_data(report_job_id)
      serid, _, dts_issue, args, _, _, _, _ = row
      if report_job_id != int(serid):
         self.dbops.update_report_data(report_job_id, -1, "BadRowID")
         return
      arr: [] = args.split(";")
      d = utils.arr_dict(arr, ":")
      self.dbops.update_report_data(report_job_id, 10, F"GOT_ARGS: {args}\n")
      try:
         backfiller: backFiller = backFiller(report_job_id, self.dbops)
         y: int = int(d["year"])
         m: int = int(d["month"])
         arr: [metCircConsumption] = backfiller.load_circuits_data(year=y, month=m)
         # -- -- -- --
         self.__save_monthly_meter_data(arr)
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         pass

   def __save_monthly_meter_data(self, arr: t.List[metCircConsumption]):
      def oneach(item: metCircConsumption):
         if not item.is_full_span or item.error_code != 0:
            print(f"UnableToSaveMonthlyReading: {item.cir_tag}")
            print(f"\tis_full_span: {item.is_full_span} | error_code : {item.error_code}")
            return
         rowid: int = self.dbops.insert_elec_met_circ_consumption(item)
         print(f"InsertRowID: {rowid} / {item.cir_tag}")
      # -- -- -- --
      for _item in arr:
         oneach(_item)
