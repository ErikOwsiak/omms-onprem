
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


class backendReportRedSub(redSubChannel):

   def __init__(self, ini: _cp.ConfigParser
         , dbops: [dbOps, None]
         , dbConnStr: str
         , red: redis.Redis):
      super().__init__(ini=ini, db=dbops, red=red)
      # -- -- -- --
      self.conn_str: str = dbConnStr
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

   def __report_thread(self, report_jobid: int):
      self.dbops: dbOps = dbOps(self.conn_str)
      row: [] = self.dbops.get_report_data(report_jobid)
      serid, _, dts_issue, args, _, _, _, _ = row
      if report_jobid != int(serid):
         self.dbops.update_report_data(report_jobid, -1, "BadRowID")
         return
      arr: [] = args.split(";")
      d = utils.arr_dict(arr, ":")
      self.dbops.update_report_data(report_jobid, 10, F"GOT_ARGS: {args}\n")
      try:
         _reportEngine: reportEngine = reportEngine(report_jobid, self.dbops)
         y: int = int(d["year"]); m: int = int(d["month"])
         arr: t.List[metCircConsumption] = _reportEngine.load_circuits_data(year=y, month=m)
         # -- -- -- --
         fixed1, dead1 = 0, 0
         fixed0, dead0 = _reportEngine.validate_try_backfill(arr)
         if fixed0 != 0:
            arr: t.List[metCircConsumption] = _reportEngine.load_circuits_data(year=y, month=m)
            fixed1, dead1 = _reportEngine.validate_try_backfill(arr)
         if fixed1 != 0:
            print("UnableToFixAllMissingDataReads")
         # -- -- -- --
         self.__save_monthly_meter_report(arr)
         rows: [] = self.dbops.get_active_clients()
         for row in rows:
            self.__save_monthly_client_report(report_jobid, y, m, row)
         # -- create xls --
         xlsout: xlsOut = xlsOut(ini=self.ini, dbops=self.dbops
            , y=y, m=m, rpt_jobid=report_jobid)
         if xlsout.init() != 0:
            pass
         xlsout.create()
         print("\n\t-- [ the end ] --")
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         pass

   def __save_monthly_meter_report(self, arr: t.List[metCircConsumption]):
      def oneach(item: metCircConsumption):
         if not item.is_full_span or item.error_code != 0:
            print(f"\nUnableToSaveMonthlyReading:: cir_tag: {item.sys_circ.cir_tag}")
            print(f"\tis_full_span:: {item.is_full_span} | error_code : {item.error_code}")
            print(f"\tsyspath: {item.sys_circ.spath}")
            return
         rowid: int = self.dbops.insert_elec_met_circ_consumption(item)
         print(f"InsertRowID: {rowid} / {item.sys_circ.cir_tag}")
      # -- -- -- --
      for _item in arr:
         oneach(_item)
      # -- -- -- --
      print("\n\t -- [ monthly electric meter update done ] --\n")

   def __save_monthly_client_report(self, rpt_jobid: int
         , y: int
         , m: int
         , clt_row: []):
      # -- -- -- --
      try:
         rowid, clt_tag, clt_name = clt_row
         _cltMon: clientMonthly = clientMonthly(self.dbops, rowid, clt_name, clt_tag)
         _cltMon.run(rpt_jobid=rpt_jobid, year=y, month=m)
      except Exception as e:
         logProxy.log_exp(["TAG_00", clt_row, e])
