
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
      ip = r.remote_addr
      b_arr: [] = [ip.startswith(n) for n in self.nets]
      accu: bool = False
      for b in b_arr:
         accu = (b or accu)
      return accu
