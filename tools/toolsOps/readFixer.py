
import sys, datetime, calendar as _cal
# -- system --
from psql.dbOps import dbOps
from core.datatypes import sysCircuit
from core.reports.kwhReading import kwhReading
from tools.toolsOps.sqlCode import sqlCode
from tools.toolsCore.utils import utils


class readFixer(object):

   def __init__(self, dbops: dbOps, cir: sysCircuit, rep_y: int, rep_m: int):
      self.dbops: dbOps = dbops
      self.cir: sysCircuit = cir
      self.rep_y = rep_y
      self.rep_m = rep_m

   def pull_data(self) -> [None, ()]:
      try:
         prv_y, prv_m = utils.prev_month(self.rep_y, self.rep_m)
         prv_row = self.dbops.get_last_of_month(self.cir.met_cir_rowid, prv_y, prv_m)
         prv_kwh: kwhReading = kwhReading("n/s", None, prv_y, prv_m, prv_row)
         # -- -- -- --
         nxt_y, nxt_m = utils.next_month(self.rep_y, self.rep_m)
         nxt_row = self.dbops.get_first_of_month(self.cir.met_cir_rowid, nxt_y, nxt_m)
         nxt_kwh: kwhReading = kwhReading("n/s", None, nxt_y, nxt_m, nxt_row)
         # -- -- -- --
         return prv_kwh, nxt_kwh
      except Exception as e:
         print(f"  -> {e}\n")
         return None

   def fix_data(self, prv_kwh: kwhReading, nxt_kwh: kwhReading):
      try:
         val: float = nxt_kwh.calc_kWhrs(prv_kwh)
         dys: int = nxt_kwh.calc_days(prv_kwh)
         daily: float = round(float(val / dys), 2)
         print(f"\t{[dys, val, daily]}")
         # -- --
         days_to_end: int = prv_kwh.days_to_lst_of_month()
         start_val: float = round(prv_kwh.tl_kwh + (days_to_end * daily) + 0.2, 2)
         # -- --
         days_to_start: int = nxt_kwh.days_to_fst_of_month()
         end_val: float = round(nxt_kwh.tl_kwh - (days_to_start * daily) + 0.2, 2)
         # -- --
         mth_val: float = round((end_val - start_val), 2)
         print(f"\t{[days_to_end, days_to_start, start_val, end_val, mth_val]}")
         # -- fix fst of the month --
         dts_s: str = f"{self.rep_y}-{self.rep_m}-1 00:02:02"
         self.dbops.backfill_kwhrs(self.cir.met_cir_rowid, start_val, dts_s)
         # -- fix lst of the month --
         last_day = utils.year_month_days(self.rep_y, self.rep_m)
         dts_e: str = f"{self.rep_y}-{self.rep_m}-{last_day} 23:58:58"
         self.dbops.backfill_kwhrs(self.cir.met_cir_rowid, end_val, dts_e)
      except Exception as e:
         print(e)
