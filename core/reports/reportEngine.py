
import datetime, typing as t
from psql.dbOps import dbOps
from core.logProxy import logProxy
from core.reports.kwhReading import kwhReading
from core.reports.metCircConsumption import metCircConsumption
from core.reports.reportsDatatypes import sysCircuitInfo


class reportEngine(object):

   def __init__(self, report_job_id: int
         , dbops: dbOps
         , tbl: str = "streams.kwhs_raw"):
      # -- -- -- --
      self.report_job_id: int = report_job_id
      self.dbops: dbOps = dbops
      self.tbl = tbl

   def run(self):
      pass

   def load_circuits_data(self, year: int, month: int) -> [metCircConsumption]:
      rows: [] = self.dbops.get_system_circuits()
      sys_circuits = [sysCircuitInfo(r) for r in rows]
      arr: t.List[metCircConsumption] = []
      for sys_circuit in sys_circuits:
         item: metCircConsumption = \
            self.__load_circuit_data(self.report_job_id, sys_circuit, year, month)
         if item is None:
            continue
         # -- -- -- --
         item.update_monthly_consumption()
         arr.append(item)
      return arr

   def validate_try_backfill(self, arr: t.List[metCircConsumption]) -> (int, int):
      fixed: int = 0; dead: int = 0
      for item in arr:
         if item.is_full_span:
            continue
         # -- -- -- --
         if not item.fst.is_fst_of_month():
            if self.backfill_fst_of_month(item.sys_circ.spath, item.fst) == 0:
               fixed += 1
            else:
               dead += 1
         if not item.lst.is_lst_of_month():
            if self.backfill_lst_of_month(item.sys_circ.spath, item.lst) == 0:
               fixed += 1
            else:
               dead += 1
         # -- -- -- --
      return fixed, dead

   def __load_circuit_data(self, report_job_id
         , sys_cir: sysCircuitInfo
         , year: int
         , month: int) -> [metCircConsumption, None]:
      try:
         rows = self.dbops.get_fst_lst_circuit_reading(sys_cir.met_circ_id, year, month)
         row_count = len(rows)
         if row_count == 0:
            return None
         elif row_count == 1:
            return None
         elif row_count == 2:
            fst_read, lst_read = \
               [kwhReading(sys_cir.cir_tag, sys_cir.met_dt_crd, year, month, i) for i in rows]
            return metCircConsumption(report_job_id, year, month, sys_cir, fst_read, lst_read)
         else:
            raise Exception("UnexpectedNumberOfRows")
      except Exception as e:
         print(e)
      finally:
         pass

   def __calc_daily_consumption(self, read: kwhReading) -> (float, int, str):
      """
         0 = {tuple: 9} (92418, 2022, datetime.datetime(2023, 2, 7, 22, 1, 19, 49540),
            False, 228.65, 8.13, 132.29, 88.23, None)
         1 = {tuple: 9} (3889, 2022, datetime.datetime(2023, 1, 25, 2, 27, 59, 958249),
            False, 218.78, 8.13, 122.67, 87.98, None)
      """
      rows: [] = self.dbops.get_neighbourhood_reads(read)
      e, s = rows
      if e[2] < s[2]:
         raise Exception("BadInput")
      # -- -- -- --
      e_kwh, s_kwh = e[4], s[4]
      if e_kwh is None and s_kwh is None:
         return None, 1, "NoDataForCalc"
      # -- -- -- --
      e_kwh = 0.0 if e[4] is None else float(e[4])
      s_kwh = 0.0 if s[4] is None else float(s[4])
      kwh = e_kwh - s_kwh
      delta: datetime.timedelta = e[2] - s[2]
      # -- -- -- --
      val: float = round(float(kwh / delta.days), 2)
      return val, 0, "OK"

   def backfill_fst_of_month(self, syspath: str, fst: kwhReading) -> int:
      try:
         daily_rate, err, msg = self.__calc_daily_consumption(fst)
         if err == 0:
            val: float = 0.0
            diff: float = daily_rate * fst.days_to_fst_of_month()
            # -- try to fix new meters --
            if fst.tl_kwh is None:
               delta: datetime.timedelta = fst.dts_utc.date() - fst.med_dt_crd
               if delta.days < 31:
                  val = daily_rate
            else:
               val = fst.tl_kwh - diff
            # -- -- -- --
            tl_kwh = "tl_kwh"
            if "pzem" in syspath:
               tl_kwh = "kWh"
            # -- -- -- --
            dtsutc: str = f"'{fst.dtsutc_fst_of_month()}'"
            _data: {} = {"PATH": syspath, tl_kwh: val}
            self.dbops.insert_elect_kwhrs_dict(fst.met_circ_id
               , _data, dtsutc, is_backfill=True, note="AUTO-BACKFILL")
            # -- -- -- --
            return 0
         else:
            print(f"\tUnableToFixMissingReadings!: {syspath}")
            return 1
      except Exception as e:
         logProxy.log_exp(e)
         return 2

   def backfill_lst_of_month(self, syspath: str, lst: kwhReading):
      try:
         daily_rate, err, msg = self.__calc_daily_consumption(lst)
         if err == 0:
            missing_days = lst.days_in_month() - lst.dts_utc.day
            add_to_kwh = missing_days * daily_rate
            lst.tl_kwh = round((lst.tl_kwh + add_to_kwh), 2)
            # -- -- -- --
            tl_kwh = "tl_kwh"
            if "pzem" in syspath:
               tl_kwh = "kWh"
            # -- -- -- --
            dtsutc: str = f"'{lst.dtsutc_lst_of_month()}'"
            _data: {} = {"PATH": syspath, tl_kwh: lst.tl_kwh}
            self.dbops.insert_elect_kwhrs_dict(lst.met_circ_id
               , _data, dtsutc, is_backfill=True, note="backfill")
            # -- -- -- --
            return 0
         else:
            print(f"\tUnableToFixMissingReadings!: {syspath}")
            return 1
      except Exception as e:
         logProxy.log_exp(e)
         return 2
