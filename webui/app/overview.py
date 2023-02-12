
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
      self.__load_meters_info()
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

   def __load_meters_info(self):
      d: {} = {}
      lastReadKey = "LAST_READ".encode()
      hours_3 = 180; hours_6 = 360
      self.red.select(redisDBIdx.DB_IDX_READS.value)
      syspaths = self.red.keys("/gdn/ck/*")
      # -- -- -- --
      for syspath in syspaths:
         d[syspath] = self.red.hgetall(syspath)
      # -- -- -- --
      ontime: [] = []; late_3h: [] = []; late_6h: [] = []
      missing: [] = []; bad_reads: [] = []
      # -- -- -- --
      def _last_read(spath, hmap: {}):
         if lastReadKey in hmap:
            spath: str = spath.decode("utf-8")
            last_read: str = hmap[lastReadKey].decode("utf-8")
            rpt_hdr, rd_stat, dtsutc = [s.strip() for s in last_read.split("|")]
            # -- -- -- --
            if rd_stat == "READ_FAILED":
               bad_reads.append(spath)
            # -- -- -- --
            dtsutc = str(dtsutc).replace("UTC", "").strip()
            dt: datetime.datetime = dateutil.parser.parse(dtsutc)
            delta: datetime.timedelta = datetime.datetime.utcnow() - dt
            minutes = int(delta.seconds / 60)
            spath = f"{spath} | {minutes} | {dtsutc}"
            if minutes < hours_3:
               ontime.append(spath)
            elif hours_3 < minutes < hours_6:
               late_3h.append(spath)
            elif minutes > hours_6:
               late_6h.append(spath)
         else:
            missing.append(syspath.decode("utf-8"))
      # -- -- -- --
      def _pong(spath: str, hmap: {}):
         pass
      # -- -- -- --
      for syspath in d.keys():
         hash_map = d[syspath]
         _last_read(syspath, hash_map)
      # -- -- -- --
      self.data["ontime"] = ontime
      self.data["late_3h"] = late_3h
      self.data["late_6h"] = late_6h
      self.data["missing"] = missing
      self.data["bad_reads"] = bad_reads
