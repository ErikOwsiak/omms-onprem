
import datetime, calendar as cal
import socket
import os, time, re
import serial, typing as t


class sysUtils(object):

   GEOLOC = ""
   BUILDING = ""
   with open("/etc/hostname") as f:
      HOST = f.read().strip()

   def __init__(self):
      pass

   @staticmethod
   def lan_ip():
      try:
         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
         s.connect(("8.8.8.8", 80))
         lanip = s.getsockname()[0]
         s.close()
         return lanip
      except Exception as e:
         print(e)

   @staticmethod
   def dts_utc(with_tz: bool = False):
      d = datetime.datetime.utcnow()
      buff = f"{d.year}-{d.month:02d}-{d.day:02d}T" \
         f"{d.hour:02d}:{d.minute:02d}:{d.second:02d}"
      return buff if with_tz is False else f"{buff} UTC"

   @staticmethod
   def ts_utc():
      _t = datetime.datetime.utcnow()
      return f"{_t.hour:02d}:{_t.minute:02d}:{_t.second:02d}"

   @staticmethod
   def syspath(channel: str, endpoint: str):
      try:
         if sysUtils.GEOLOC == "":
            with open("/etc/iotech/geoloc") as f:
               sysUtils.GEOLOC = f.read().strip()
         if sysUtils.BUILDING == "":
            with open("/etc/iotech/building") as f:
               sysUtils.BUILDING = f.read().strip()
         if sysUtils.HOST == "":
            with open("/etc/hostname") as f:
               sysUtils.HOST = f.read().strip()
         # -- -- -- --
         return f"/{sysUtils.GEOLOC}/{sysUtils.BUILDING}/{sysUtils.HOST}/{channel}/{endpoint}"
      except Exception as e:
         print(e)
         exit(1)

   @staticmethod
   def min_dts() -> datetime.datetime:
      return datetime.datetime.fromisoformat("0001-01-01T01:01:01")

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

   @staticmethod
   def pin_redis_key(devid: str, chnl: int):
      return f'PIN_{devid}_ch_{chnl}'.upper()

   @staticmethod
   def decode_redis(src):
      if isinstance(src, list):
         rv = list()
         for key in src:
            rv.append(sysUtils.decode_redis(key))
         return rv
      elif isinstance(src, dict):
         rv = dict()
         for key in src:
            rv[key.decode()] = sysUtils.decode_redis(src[key])
         return rv
      elif isinstance(src, bytes):
         return src.decode()
      else:
         raise Exception("type not handled: " + type(src))
