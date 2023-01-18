
import os, json, configparser as _cp, redis
from psycopg2.extensions import connection as _psql_conn
from psql.dbOps import dbOps

class apiOps(object):

   def __init__(self, INI: _cp.ConfigParser
         , conn: _psql_conn = None
         , red: redis.Redis = None):
      # -- -- -- -- -- -- -- --
      self.ini: _cp.ConfigParser = INI
      self.conn = conn
      self.red: redis.Redis = red
      self.dbops: dbOps = dbOps(self.conn)

   @staticmethod
   def list_reports() -> str:
      files: {} = {}
      path = "www/reports"
      dirs: [] = [fi for fi in os.scandir(path) if fi.is_dir()]
      for d in dirs:
         fls = [fi.name for fi in os.scandir(d) if not fi.is_dir() and fi.name.endswith(".xlsx")]
         files[d.name] = fls
      # -- push out all files --
      return json.dumps(files)

   def list_clients(self) -> str:
      arr = self.dbops.get_active_clients()
      return json.dumps(arr)
