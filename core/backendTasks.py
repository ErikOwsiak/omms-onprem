
import calendar as _cal
import logging, datetime, dateutil
import redis, configparser as _cp, smtplib
from email.message import EmailMessage
from dateutil.parser import parser
from ommslib.shared.core.datatypes import redisDBIdx, readStatus
from psql.dbOps import dbOps
from core.utils import sysUtils as utils


class backendTasks(object):

   RED_ALERT_KEY: str = "ALERT_LAST_SENT_DTS"
   ALERT_TASK_DATA: str = "ALERT_TASK_DATA"
   INI_ALERT_SEND_ON: str = "ALERT_SEND_ON"

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

   def init(self):
      if self.red is not None:
         self.red.select(redisDBIdx.DB_IDX_RUNTIME.value)
         self.red.delete(backendTasks.ALERT_TASK_DATA)

   def check_late_reads(self) -> int:
      try:
         data: {} = self._load_meters_info()
         late3h = data["late_3h"]
         late6h = data["late_6h"]
         # -- -- -- --
         has_lates: bool = (len(late3h) > 0 or len(late6h) > 0)
         time_slot = self._get_timeslot_to_send_alert()
         if has_lates and time_slot is not None:
            if self._send_alert(data):
               self.red.select(redisDBIdx.DB_IDX_RUNTIME.value)
               d: {} = {time_slot.upper(): utils.dts_utc()}
               self.red.hset(backendTasks.ALERT_TASK_DATA, mapping=d)
         else:
            self.red.select(redisDBIdx.DB_IDX_RUNTIME.value)
            ini_key_val = self.ini.get("BACKEND", backendTasks.INI_ALERT_SEND_ON)
            d: {} = {"LAST_RUN": utils.dts_utc(with_tz=True)
               , "IS_TIME_TO_RUN": "NO"
               , "INI_ALERT_SEND_ON": ini_key_val}
            self.red.hset(backendTasks.ALERT_TASK_DATA, mapping=d)
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
            logging.error(e)
      # -- -- -- --
      def _read_status(keys: [], spath, hmap: {}):
         try:
            # -- -- -- --
            keys_out = []
            spath: str = spath.decode("utf-8")
            for key in keys:
               if key not in hmap:
                  print(f"\tKeyNotFound: {key} in hmap")
                  continue
               read_stat: str = hmap[key]
               _, _, stat = [s.strip() for s in read_stat.split("|")]
               if stat == readStatus.READ_OK:
                  continue
               keys_out.append(key)
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
            missing.append(syspath)
      # -- -- -- --
      dout: {} = {"ontime": ontime, "late_3h": late_3h
         , "late_6h": late_6h, "missing": missing, "bad_reads": bad_reads}
      # -- -- -- --
      return dout

   def _get_timeslot_to_send_alert(self) -> [None, str]:
      # -- -- -- --
      def _is_good_slot(ts: str, td: {}) -> bool:
         slot_dow, slot_time = ts.split(":")
         dt_now: datetime.datetime = datetime.datetime.utcnow()
         if slot_dow.upper() == dt_now.strftime("%A").upper():
            dict_key: bytes = ts.upper().encode()
            if dict_key in td.keys():
               v: str = td[dict_key]
               _d = dateutil.parser.parse(v)
               return not self._was_run_today(dt_now, _d)
            else:
               h, m = slot_time[:2], slot_time[2:]
               stime: datetime.time = datetime.time(hour=int(h), minute=int(m))
               return dt_now.time() > stime
         else:
            return False
      # -- -- -- --
      alert_send_on = self.ini.get("BACKEND", backendTasks.INI_ALERT_SEND_ON)
      if alert_send_on is None:
         return True
      # -- -- -- --
      self.red.select(redisDBIdx.DB_IDX_RUNTIME.value)
      task_data = self.red.hgetall(backendTasks.ALERT_TASK_DATA)
      if task_data is None:
         task_data: {} = {}
      # -- -- -- --
      time_slots = [s.strip() for s in alert_send_on.split(",")]
      for time_slot in time_slots:
         if _is_good_slot(time_slot, task_data):
            return time_slot
      # -- -- -- --
      return None

   def _send_alert(self, data: {}) -> bool:
      to_emails: str = self.ini.get("BACKEND", "ALERT_EMAILS")
      emsg: EmailMessage = EmailMessage()
      emsg["Subject"] = "OMMS Alert"
      emsg["From"] = "system@iotech.systems"
      emsg["To"] = to_emails
      emsg["Cc"] = "omms.bot@iotech.systems"
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

   def _was_run_today(self, d0: datetime.datetime, d1: datetime.datetime):
      bool_date: bool = (d0.year == d1.year) and \
         (d0.month == d1.month) and (d0.day == d1.day)
      if bool_date is False:
         return False
      # -- -- -- --
      bool_time: bool = d0.time() >= d1.time()
      return bool_date and bool_time
