
import calendar as cal
import datetime


# (22874, 2069, datetime.datetime(2023, 1, 31, 4, 6, 24, 634532)
#  , False, 5828.86, 3744.46, 1246.18, 838.22, None)
class kwhReading(object):

   def __init__(self, cir_tag
         , med_dt_crd: datetime.date
         , year
         , month
         , row):
      # -- -- -- -- -- -- -- --
      self.cir_tag = cir_tag
      self.med_dt_crd: datetime.date = med_dt_crd
      self.year = year
      self.month = month
      self.read_id = row[0]
      self.met_circ_id = row[1]
      self.dts_utc: datetime.datetime = row[2]
      self.dts_utc.replace(microsecond=0)
      self.is_backfill = row[3]
      self.tl_kwh = row[4]
      self.l1_kwh = row[5]
      self.l2_kwh = row[6]
      self.l3_kwh = row[7]
      self.note = row[8]
      self.is_full_span: bool = False
      self.msg: str = ""

   def is_lst_of_prev_month(self) -> bool:
      return True

   def is_fst_of_month(self) -> bool:
      return self.dts_utc.day == 1

   def is_lst_of_month(self) -> bool:
      _, days = cal.monthrange(self.dts_utc.year, self.dts_utc.month)
      return self.dts_utc.day == days

   def days_to_fst_of_month(self) -> int:
      return self.dts_utc.day

   def days_to_lst_of_month(self) -> int:
      y, m = self.dts_utc.year, self.dts_utc.month
      _, days = cal.monthrange(y, m)
      return days - self.dts_utc.day

   def dtsutc_fst_of_month(self):
      return f"{self.year}-{self.month:02d}-01 00:02:02"

   def dtsutc_lst_of_month(self):
      y, m = self.dts_utc.year, self.dts_utc.month
      _, d = cal.monthrange(y, m)
      return f"{self.year}-{self.month:02d}-{d:02d} 23:58:58"

   def days_in_month(self) -> int:
      y, m = self.dts_utc.year, self.dts_utc.month
      _, d = cal.monthrange(y, m)
      return d

   def calc_kWhrs(self, other) -> [None, float]:
      other: kwhReading = other
      if self.tl_kwh is None or other.tl_kwh is None:
         self.msg = "OneOfInputsIsNone"
         return None
      return self.tl_kwh - other.tl_kwh

   def info(self) -> str:
      return f"{self.cir_tag}; {self.tl_kwh}; {self.dts_utc.replace(microsecond=0)}"
