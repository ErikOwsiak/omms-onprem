
import json, redis
import dateutil.parser, datetime
from ommslib.shared.core.datatypes import redisDBIdx
from ommslib.shared.utils.sunclock import sunClock
from ommslib.shared.utils.locationTxtInfo import locationTxtInfo


class sysOverview(object):

   def __init__(self, red: redis.Redis):
      self.red: redis.Redis = red
      self.data: {} = None

   def load(self) -> bool:
      # -- get: sunrise; sunset; --
      self.__load_sun_info()
      # -- pull from red by all syspaths --
      self.__load_meter_info()
      return True

   def to_json_str(self) -> str:
      self.data["error"] = 0
      return json.dumps(self.data)

   def __load_sun_info(self):
      locfile = "conf/location.txt"
      locInfo: locationTxtInfo = locationTxtInfo(locfile)
      if not locInfo.load():
         pass
      sunClk: sunClock = sunClock(locInfo)
      sunrise = sunClk.get_time_v1("sunrise")
      sunset = sunClk.get_time_v1("sunset")
      self.data = {"sunrise": str(sunrise), "sunset": str(sunset)}

   def __load_meter_info(self):
      hours_3 = 180; hours_6 = 360
      d: {} = {}
      self.red.select(redisDBIdx.DB_IDX_READS.value)
      syspaths = self.red.keys("/gdn/ck/*")
      # -- -- -- --
      for syspath in syspaths:
         d[syspath] = self.red.hgetall(syspath)
      # -- -- -- --
      ontime: [] = []; late_3h: [] = []; late_6h: [] = []; missing: [] = []
      bKey = "LAST_READ".encode()
      for syspath in d.keys():
         hash_map = d[syspath]
         if bKey in hash_map:
            last_read = hash_map[bKey].decode("utf-8")
            dt: datetime.datetime = dateutil.parser.parse(last_read)
            delta: datetime.timedelta = datetime.datetime.utcnow() - dt
            minutes = int(delta.seconds / 60)
            spath = syspath.decode("utf-8") + f" | {minutes} | {last_read}"
            if minutes < hours_3:
               ontime.append(spath)
            elif hours_3 < minutes < hours_6:
               late_3h.append(spath)
            elif minutes > hours_6:
               late_6h.append(spath)
         else:
            missing.append(syspath.decode("utf-8"))
      # -- -- -- --
      self.data["ontime"] = ontime
      self.data["late_3h"] = late_3h
      self.data["late_6h"] = late_6h
      self.data["missing"] = missing
