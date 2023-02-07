
import calendar as cal
import datetime


# (22874, 2069, datetime.datetime(2023, 1, 31, 4, 6, 24, 634532)
#  , False, 5828.86, 3744.46, 1246.18, 838.22, None)
class kwhReading(object):

   def __init__(self, cir_tag, y, m, row):
      self.cir_tag = cir_tag
      self.year = y
      self.month = m
      self.read_id = row[0]
      self.met_circ_id = row[1]
      self.dts_utc: datetime.datetime = row[2]
      self.is_backfill = row[3]
      self.tl_kwh = row[4]
      self.l1_kwh = row[5]
      self.l2_kwh = row[6]
      self.l3_kwh = row[7]
      self.note = row[8]
      self.is_full_span: bool = False
      self.msg: str = ""

   def is_fst_of_month(self):
      return self.dts_utc.day == 1

   def is_lst_of_month(self):
      _, days = cal.monthrange(self.dts_utc.year, self.dts_utc.month)
      return self.dts_utc.day == days

   def calc_kWhrs(self, other) -> [None, float]:
      other: kwhReading = other
      if self.tl_kwh is None or other.tl_kwh is None:
         self.msg = "OneOfInputsIsNone"
         return None
      return self.tl_kwh - other.tl_kwh

   def info(self) -> str:
      return f"cir_tag: {self.cir_tag} | tl_kwh: {self.tl_kwh} | dts_utc: {self.dts_utc}"
