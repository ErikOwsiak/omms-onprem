
from psql.dbOps import dbOps
from core.logProxy import logProxy
from core.reports.reportsDatatypes import clientReport
from core.utils import sysUtils as utils


class clientMonthly(object):

   def __init__(self, dbops: dbOps, clt_dbid: int, clt_name: str, clt_tag: str):
      self.dbops: dbOps = dbops
      self.clt_dbid = clt_dbid
      self.clt_name = clt_name
      self.clt_tag = clt_tag
      self.report_jobid = None
      self.year = None
      self.month = None
      self.data: [] = None

   def int(self):
      pass

   def run(self, **kwargs):
      self.report_jobid = int(kwargs["rpt_jobid"])
      self.year: int = int(kwargs["year"])
      self.month: int = int(kwargs["month"])
      self.data: [] = self.__load_data()
      rval = self.__process_data()

   def __load_data(self) -> []:
      clt_cirs = self.dbops.get_client_circuits(self.clt_tag)
      cir_reports: [] = []
      # -- -- -- --
      def __oneach():
         try:
            row_sid, locl_tag, cir_tag, met_syspath, code = clt_cir
            rpt: [] = self.dbops.get_circuit_report(cir_tag, self.report_jobid
               , self.year, self.month)
            if rpt is not None:
               cir_reports.append(rpt)
            else:
               cir_reports.append((cir_tag, met_syspath, code, "NoReportDataIn::[ __load_data ]"))
         except Exception as e:
            logProxy.log_exp([clt_cir, e])
         finally:
            pass
      # -- -- -- --
      for clt_cir in clt_cirs:
        __oneach()
      # -- -- -- --
      return cir_reports

   def __process_data(self) -> ():
      reps: [] = []; total_kwh: float = 0.0
      for item in self.data:
         try:
            if item is not None and len(item) == 12:
               row_serid, met_circ_dbid, cir_tag, report_jobid, error, error_msg,\
                  year, month, fst_input, lst_input, consumed_kwh, dts_crd = item
               total_kwh += float(consumed_kwh)
               reps.append(f"{fst_input} | {lst_input}")
            else:
               logProxy.log_exp(item)
         except Exception as e:
            logProxy.log_exp(["TAG_0002", item, e])
      # -- save --
      calc_notes = " && ".join(reps)
      r: clientReport = clientReport(self.clt_dbid, self.report_jobid
         , self.clt_tag, self.clt_name, self.year, self.month
         , total_kwh, calc_notes)
      # -- -- -- --
      rowid: int = self.dbops.insert_client_kwhrs_consumption(r)
      if rowid > 0:
         return round(total_kwh, 2), calc_notes
      else:
         return -1.0, None
