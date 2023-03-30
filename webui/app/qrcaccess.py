
import datetime, os.path
import redis, uuid, qrcode
from flask import Request as _req


class qrcAccess(object):

   DT_FORMAT = "%Y:%m:%d %H:%M"

   def __init__(self, red: redis.Redis, red_db_idx: int):
      self.red: redis.Redis = red
      self.db_idx: int = red_db_idx

   def create_new_qrc(self, url_path, fs_path: str) -> (bool, str, str):
      # -- -- -- --
      hex_buff: str = uuid.uuid4().hex
      qrc: qrcode.QRCode = qrcode.QRCode(version=1
         , error_correction=qrcode.constants.ERROR_CORRECT_L
         , box_size=8, border=4)
      # -- -- -- --
      data: str = f"{url_path}/api/qrc/validate/{hex_buff}"
      qrc.add_data(data)
      qrc.make(fit=True)
      img: qrcode.image = qrc.make_image(fill_color="black", back_color="white")
      if os.path.exists(fs_path):
         os.unlink(fs_path)
      # -- -- -- --
      img.save(fs_path)
      return True, hex_buff, data

   def create_temp_object(self, ip_addr, num: int, numt: str, _uuid) -> (str, int):
      ttl = 60
      now_utc = datetime.datetime.utcnow()
      multi: int = 1 if (numt.upper() == "H") else 24
      expr_hrs: int = num * multi
      dt: datetime.datetime = now_utc + datetime.timedelta(hours=expr_hrs)
      dt_str: str = dt.strftime(qrcAccess.DT_FORMAT)
      d: {} = {"REQ_IP": ip_addr, "NUM": num, "NUMT": numt
         , "EXPIRES_UTC": dt_str, "UUID": _uuid}
      self.red.select(self.db_idx)
      self.red.hset(_uuid, mapping=d)
      self.red.expire(_uuid, (ttl + 4))
      return _uuid, ttl

   def validate_qrc(self, _uuid: str) -> (int, str):
      self.red.select(self.db_idx)
      red_hash = self.red.hgetall(_uuid)
      if red_hash is None or len(red_hash.keys()) == 0:
         return 1, None    # not found
      # -- -- -- --
      exp: str = red_hash["EXPIRES_UTC"]
      exp_dt: datetime.datetime = datetime.datetime.strptime(exp, qrcAccess.DT_FORMAT)
      t_delt: datetime.timedelta = exp_dt - datetime.datetime.utcnow()
      self.red.expire(_uuid, t_delt)
      return 0, exp

   def check_auth(self, red_webui_key: str
         , req: _req
         , cookie_name: str):
      # -- -- -- --
      auth = req.cookies.get(cookie_name)
      print(auth)
