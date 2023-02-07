
import datetime, calendar as cal
from psql.dbOps import dbOps
from core.reports.kwhReading import kwhReading
from core.reports.metCircConsumption import metCircConsumption


class backFiller(object):

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
      sys_circuits: [] = self.dbops.get_system_circuits()
      arr: [metCircConsumption] = []
      for sys_circuit in sys_circuits:
         met_cir_id, cir_tag, spath, elecrm = sys_circuit
         item: metCircConsumption = self.__load_circuit_data(self.report_job_id, met_cir_id, cir_tag, year, month)
         item.update_monthly_consumption()
         arr.append(item)
      return arr

   def __load_circuit_data(self, report_job_id
         , met_cir_id: int
         , cir_tag: str
         , year: int
         , month: int) -> [metCircConsumption, None]:
      try:
         rows = self.dbops.get_fst_lst_circuit_reading(met_cir_id, year, month)
         row_count = len(rows)
         if row_count == 0:
            return None
         elif row_count == 1:
            return None
         elif row_count == 2:
            fst_read, lst_read = [kwhReading(cir_tag, year, month, i) for i in rows]
            return metCircConsumption(report_job_id, year, month, fst_read, lst_read)
         else:
            raise Exception("UnexpectedNumberOfRows")
      except Exception as e:
         print(e)
      finally:
         pass

   def __fst_previous_reading(self, dt: datetime.date) -> [(), None]:
      sdate = f"{dt.year}-{dt.month:02d}-{dt.day:02d}"
      qry = f"select t.fk_meter_dbid, t.reading_dts_utc, t.total_kwhrs" \
         f" from streams.{self.tbl} t where t.fk_meter_dbid = {self.meter_dbid}" \
         f" and t.reading_dts_utc < '{sdate}' order by t.reading_dts_utc desc limit 1;"
      arr: [] = self.db_ref.qry_arr(qry)
      if len(arr) > 0:
         return arr[0]
      else:
         return None

   def __fst_next_reading(self, dt: datetime.date) -> [(), None]:
      sdate = f"{dt.year}-{dt.month:02d}-{dt.day:02d}"
      qry = f"""select t.fk_meter_dbid, t.reading_dts_utc, t.total_kwhrs
         from streams.{self.tbl} t where t.fk_meter_dbid = {self.meter_dbid} 
         and t.reading_dts_utc > '{sdate}' order by t.reading_dts_utc asc limit 1;"""
      arr: [] = self.db_ref.qry_arr(qry)
      if len(arr) > 0:
         return arr[0]
      else:
         return None

   def backfill_fst_of_month(self, dt: datetime.date):
      # -- -- -- --
      print(f"\n\t[ backfill_fst_of_month: {dt.year}/{dt.month}/{dt.day} ]")
      # -- -- -- --
      __fst_pre_tup = self.__fst_previous_reading(dt)
      if __fst_pre_tup is None:
         return False
      # -- -- -- --
      __fst_nxt_tup = self.__fst_next_reading(dt)
      if __fst_nxt_tup is None:
         return False
      # -- needed info --
      print(["__fst_pre_tup", __fst_pre_tup])
      print(["__fst_nxt_tup", __fst_nxt_tup])
      # -- do --
      p_dbid, p_dts, p_tkwhrs = __fst_pre_tup
      n_dbid, n_dts, n_tkwhrs = __fst_nxt_tup
      # -- get # of days --
      tdt: datetime.timedelta = (n_dts - p_dts)
      daily: float = round(((n_tkwhrs - p_tkwhrs) / tdt.days), 6)
      # -- days from rst reading to the 1st of current month --
      p_dts: datetime.datetime = p_dts
      xdt: datetime.timedelta = (dt - p_dts.date())
      t_kwhrs: float = round(((daily * xdt.days) + p_tkwhrs), 4)
      # -- insert on the last day of prev month --
      pdt: datetime.date = dt - datetime.timedelta(days=-1)
      dts = f"{pdt.year}-{pdt.month:02d}-{pdt.day:02d} 23:59:52"
      qry = f"insert into streams.{self.tbl}" \
            f" values (default, {p_dbid}, true, '{dts}', 0.22, {t_kwhrs}, 0,0,0, now());"
      # -- insert on the 1st day of the current month --
      v0 = self.db_ref.insert_1row(qry)
      dts = f"{dt.year}-{dt.month:02d}-01 00:01:01"
      qry = f"insert into streams.{self.tbl}" \
         f" values (default, {p_dbid}, true, '{dts}', 0.22, {t_kwhrs}, 0, 0, 0, now());"
      v1 = self.db_ref.insert_1row(qry)
      # -- the end --
      return True

   def backfill_lst_of_month(self, dt: datetime.date) -> bool:
      # -- -- -- --
      print(f"\n\t[ backfill_lst_of_month: {dt.year}/{dt.month}/{dt.day} ]")
      # -- -- -- --
      __fst_pre_tup = self.__fst_previous_reading(dt)
      if __fst_pre_tup is None:
         return False
      # -- -- -- --
      __fst_nxt_tup = self.__fst_next_reading(dt)
      if __fst_nxt_tup is None:
         return False
      # -- needed info --
      print(["__fst_pre_tup", __fst_pre_tup])
      print(["__fst_nxt_tup", __fst_nxt_tup])
      # -- do --
      p_dbid, p_dts, p_tkwhrs = __fst_pre_tup
      n_dbid, n_dts, n_tkwhrs = __fst_nxt_tup
      # -- get # of days --
      tdt: datetime.timedelta = (n_dts - p_dts)
      daily: float = round(((n_tkwhrs - p_tkwhrs) / tdt.days), 6)
      _, _days = cal.monthrange(dt.year, dt.month)
      t_kwhrs: float = round(((daily * _days) + p_tkwhrs), 4)
      # -- insert on the lst day of the current month --
      dts = f"{dt.year}-{dt.month:02d}-{dt.day:02d} 23:59:52"
      qry = f"insert into streams.{self.tbl}" \
         f" values (default, {p_dbid}, true, '{dts}', 0.22, {t_kwhrs}, 0, 0, 0, now());"
      v0 = self.db_ref.insert_1row(qry)
      pdt: datetime.date = dt + datetime.timedelta(days=1)
      dts = f"{pdt.year}-{pdt.month:02d}-{pdt.day:02d} 00:01:01"
      qry = f"insert into streams.{self.tbl}" \
         f" values (default, {p_dbid}, true, '{dts}', 0.22, {t_kwhrs}, 0, 0, 0, now());"
      v1 = self.db_ref.insert_1row(qry)
      # -- the end --
      return True
