
import redis, configparser as _cp
from flask import Request as _req


class auth(object):

   def __init__(self, ini: _cp.ConfigParser
         , red: redis.Redis):
      # -- -- -- --
      self.ini: _cp.ConfigParser = ini
      self.red: redis.Redis = red
      _nets: [] = self.ini.get("HTTP", "ALLOWED_HOSTS").split(",")
      self.nets = [n.replace("*", "").strip() for n in _nets]

   def check_net(self, r: _req) -> bool:
      # -- -- -- --
      remote_ip = r.headers.get("X-Forwarded-For")
      if remote_ip in [None, ""]:
         remote_ip = r.remote_addr
      # -- -- -- --
      for n in self.nets:
         if remote_ip.startswith(n):
            print(f"[ GOOD_IP: {remote_ip} -> MATCH_ON: {n} ]")
            return True
      # -- -- -- --
      return False
