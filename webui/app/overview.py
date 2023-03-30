
import json, redis
import dateutil.parser, datetime
from psql.dbOps import dbOps
from core.logProxy import logProxy
from ommslib.shared.core.datatypes import redisDBIdx, readStatus
from ommslib.shared.utils.sunclock import sunClock
from ommslib.shared.utils.locationTxtInfo import locationTxtInfo


class sysOverview(object):

   def __init__(self, dbops: dbOps
         , red: redis.Redis):
      # -- -- -- --
      self.dbops: dbOps = dbops
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
      kwhReadKey = "#RPT_kWhrs_STATUS".encode()
      pwrReadKey = "#RPT_powerStats_STATUS".encode()
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
      def _timing_read(spath, hmap: {}):
         try:
            spath: str = spath
            last_read: str = hmap[lastReadKey]
            _, _, dtsutc = [s.strip() for s in last_read.split("|")]
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
         except Exception as e:
            logProxy.log_exp(e)
      # -- -- -- --
      def _read_status(keys: [], spath, hmap: {}):
         try:
            # -- -- -- --
            keys_out = []
            spath: str = spath
            for key in keys:
               read_stat: str = hmap[key]
               _, _, stat = [s.strip() for s in read_stat.split("|")]
               # -- -- -- --
               if stat == readStatus.READ_OK:
                  continue
               keys_out.append(key)
            # -- -- -- --
            if len(keys_out) > 0:
               ltag, ctag = self.dbops.get_syspath_info(spath)
               ltag, ctag = ["n/s" if s is None else s for s in (ltag, ctag)]
               m: str = f"{spath} <br/> " + " | ".join(keys_out) + "<br/>" + " | ".join([ltag, ctag])
               bad_reads.append(m)
         except Exception as e:
            logProxy.log_exp(e)
      # -- -- -- --
      for syspath in d.keys():
         hash_map = d[syspath]
         if hash_map:
            _timing_read(syspath, hash_map)
            _read_status([kwhReadKey, pwrReadKey], syspath, hash_map)
         else:
            missing.append(syspath)
      # -- -- -- --
      self.data["ontime"] = ontime
      self.data["late_3h"] = late_3h
      self.data["late_6h"] = late_6h
      self.data["missing"] = missing
      self.data["bad_reads"] = bad_reads
