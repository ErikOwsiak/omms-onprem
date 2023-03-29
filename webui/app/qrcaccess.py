
import os.path
import redis, uuid, qrcode


class qrcAccess(object):

   def __init__(self, red: redis.Redis, red_db_idx: int):
      self.red: redis.Redis = red
      self.db_idx: int = red_db_idx

   def create_new_qrc(self, url_path, fs_path: str) -> (bool, str):
      # -- -- -- --
      hex_buff: str = uuid.uuid4().hex
      qrc: qrcode.QRCode = qrcode.QRCode(version=1
         , error_correction=qrcode.constants.ERROR_CORRECT_L
         , box_size=8, border=4)
      # -- -- -- --
      d: str = f"{url_path}/api/qrc/validate/{hex_buff}"
      qrc.add_data(d)
      qrc.make(fit=True)
      img: qrcode.image = qrc.make_image(fill_color="black", back_color="white")
      if os.path.exists(fs_path):
         os.unlink(fs_path)
      # -- -- -- --
      img.save(fs_path)
      return True, hex_buff

   def create_temp_object(self, ip_addr, num, numt, xuuid) -> (str, int):
      ttl = 60
      key: str = f"QRC_REQ_{ip_addr}".upper()
      d: {} = {"REQ_IP": ip_addr, "NUM": num, "NUMT": numt, "UUID": xuuid}
      self.red.select(self.db_idx)
      self.red.hset(key, mapping=d)
      self.red.expire(key, ttl)
      return key, ttl
