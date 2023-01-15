
import configparser as _cp
from psql.dbOps import dbOps


class redSubChannel(object):

   def __init__(self, ini: _cp.ConfigParser, db: dbOps):
      self.ini: _cp.ConfigParser = ini
      self.dbops: dbOps = db
      self.sub_channel: str = ""

   def init(self):
      pass

   def on_msg(self,  msg: {}):
      pass
