
import logging, datetime, dateutil
import redis, configparser as _cp, smtplib
from email.message import EmailMessage
from dateutil.parser import parser
from ommslib.shared.core.datatypes \
   import redisDBIdx, readStatus
from psql.dbOps import dbOps
from core.utils import sysUtils as utils


class backendTasks(object):

   RED_ALERT_KEY = "ALERT_LAST_SENT_DTS"

   def __init__(self, INI: _cp.ConfigParser
         , red: redis.Redis
         , dbops: dbOps
         , conn_str: str = None):
      # -- -- -- --
      self.ini = INI
      self.red: redis.Redis = red
      self.dbops: dbOps = dbops
      self._conn_str = conn_str

   def __del__(self):
      pass

   def check_late_reads(self) -> int:
      try:
         data: {} = self._load_meters_info()
         late3h = data["late_3h"]
         late6h = data["late_6h"]
         # bad_reads = data["bad_reads"]
         # -- -- -- --
         if len(late3h) > 0 or len(late6h) > 0 and self._is_time_to_send_alert():
            if self._send_alert(data):
               self.red.select(redisDBIdx.DB_IDX_RUNTIME.value)
               self.red.set(backendTasks.RED_ALERT_KEY, utils.dts_utc())
         else:
            pass
         # -- -- -- --
         return 0
      except Exception as e:
         logging.error(e)
         return 1
      finally:
         pass

   def _load_meters_info(self) -> {}:
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
            spath: str = spath.decode("utf-8")
            last_read: str = hmap[lastReadKey].decode("utf-8")
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
            logging.error(e)
      # -- -- -- --
      def _read_status(keys: [], spath, hmap: {}):
         try:
            # -- -- -- --
            keys_out = []
            spath: str = spath.decode("utf-8")
            for key in keys:
               read_stat: str = hmap[key].decode("utf-8")
               _, _, stat = [s.strip() for s in read_stat.split("|")]
               # -- -- -- --
               if stat == readStatus.READ_OK:
                  continue
               keys_out.append(key.decode("utf-8"))
            # -- -- -- --
            if len(keys_out) > 0:
               ltag, ctag = self.dbops.get_syspath_info(spath)
               ltag, ctag = ["n/s" if s is None else s for s in (ltag, ctag)]
               m: str = f"{spath}" + " | ".join(keys_out) + " | ".join([ltag, ctag])
               bad_reads.append(m)
         except Exception as e:
            logging.error(e)
      # -- -- -- --
      for syspath in d.keys():
         hash_map = d[syspath]
         if hash_map:
            _timing_read(syspath, hash_map)
            _read_status([kwhReadKey, pwrReadKey], syspath, hash_map)
         else:
            missing.append(syspath.decode("utf-8"))
      # -- -- -- --
      dout: {} = {"ontime": ontime, "late_3h": late_3h
         , "late_6h": late_6h, "missing": missing, "bad_reads": bad_reads}
      # -- -- -- --
      return dout

   def _is_time_to_send_alert(self):
      self.red.select(redisDBIdx.DB_IDX_RUNTIME.value)
      val = self.red.get(backendTasks.RED_ALERT_KEY)
      if val is None:
         return True
      # -- -- -- --
      utc = utils.dts_utc()
      now: datetime.datetime = dateutil.parser.parse(utc)
      dts = dateutil.parser.parse(val.decode("utf-8"))
      diff = now - dts
      return diff.seconds > 3600

   def _send_alert(self, data: {}) -> bool:
      to_emails: str = self.ini.get("BACKEND", "ALERT_EMAILS")
      emsg: EmailMessage = EmailMessage()
      emsg["Subject"] = "OMMS Alert"
      emsg["From"] = "system@iotech.systems"
      emsg["To"] = to_emails
      emsg["Cc"] = "system.out@iotech.systems"
      msg = self._create_msg_body(data)
      emsg.set_content(msg)
      try:
         smtp_conf: str = self.ini.get("BACKEND", "ALERT_SERVER")
         host, port, uid, pwd = [s.strip() for s in smtp_conf.split(";")]
         sess = smtplib.SMTP(host=host, port=int(port))
         sess.starttls()
         sess.login(user=uid, password=pwd)
         sess.send_message(msg=emsg)
         sess.close()
         return True
      except Exception as e:
         logging.error(e)
         return False

   def _create_msg_body(self, data: {}) -> str:
      buff: [] = ["OMMS Alert Report:\n"]
      for k in data.keys():
         buff.append(k)
         arr: [] = [f"\t{x}" for x in data[k]]
         buff.extend(arr)
      # -- -- -- --
      return "\n".join(buff)
