
import redis
import configparser as _cp
from psql.dbOps import dbOps


class redSubChannel(object):

   def __init__(self, ini: _cp.ConfigParser, db: dbOps, red: redis.Redis = None):
      self.ini: _cp.ConfigParser = ini
      self.dbops: dbOps = db
      self.red: redis.Redis = red
      self.chnl_pattern: str = ""

   def init(self):
      pass

   def on_msg(self,  msg: {}):
      pass
