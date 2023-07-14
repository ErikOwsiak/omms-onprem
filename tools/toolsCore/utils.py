
import calendar as cal
import datetime, time


class utils(object):

   @staticmethod
   def next_month_day_date(y: int, m: int, d: int = 1) -> datetime.date:
      if m == 12:
         y += 1
         m = 1
      # -- return date --
      return datetime.date(y, m, d)

   @staticmethod
   def next_month_day_str(y: int, m: int, d: int = 1) -> str:
      if m == 12:
         y += 1; m = 1
      else:
         m += 1
      # -- return date --
      return f"{y}-{m:02d}-{d:02d}"

   @staticmethod
   def prev_month(y: int, m: int) -> ():
      if m not in range(1, 13):
         raise Exception("MonthInputOutOfRange")
      if m in range(2, 13):
         return y, (m - 1)
      else:
         return (y - 1), 12

   @staticmethod
   def next_month(y: int, m: int) -> ():
      if m not in range(1, 13):
         raise Exception("MonthInputOutOfRange")
      if m in range(1, 12):
         return y, (m + 1)
      else:
         return (y + 1), 1

   @staticmethod
   def dts_now():
      d = datetime.datetime.utcnow()
      return f"{d.year}-{d.month:02d}-{d.day:02d}" \
         f" {d.hour:02d}:{d.minute:02d}:{d.second:02d}"

   @staticmethod
   def get_run_id():
      tme = int(time.time())
      return f"0x{tme:08x}"

   @staticmethod
   def year_month_days(y: int, m: int):
      return cal.monthrange(y, m)[1]
