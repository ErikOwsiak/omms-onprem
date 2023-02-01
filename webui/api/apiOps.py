
import os, json, configparser as _cp, redis
# from psycopg2.extensions import connection as _psql_conn
# from psql.dbConnServer import dbConnServer
from psql.dbOps import dbOps


class apiOps(object):

   RPTS_FOLDER = None

   def __init__(self, INI: _cp.ConfigParser
         , conn_str: str
         , red: redis.Redis = None):
      # -- -- -- -- -- -- -- --
      self.ini: _cp.ConfigParser = INI
      self.conn_str: str = conn_str
      self.red: redis.Redis = red
      self.dbops: dbOps = dbOps(conn_str=self.conn_str)
      self.reports_fld = self.ini.get("WEBUI", "REPORTS_FOLDER")
      apiOps.RPTS_FOLDER = self.reports_fld

   def list_reports(self) -> str:
      files: {} = {}
      elc_rpt_fld = f"{self.reports_fld}/electric"
      dirs: [] = [fi for fi in os.scandir(elc_rpt_fld) if fi.is_dir()]
      for d in dirs:
         fls = [fi.name for fi in os.scandir(d) if not fi.is_dir() and fi.name.endswith(".xlsx")]
         files[d.name] = fls
      # -- push out all files --
      return json.dumps(files)

   def list_clients(self) -> str:
      arr = self.dbops.get_active_clients()
      return json.dumps(arr)

   def list_client_circuits(self, clt_tag: str):
      arr = self.dbops.get_client_circuits(clt_tag)
      return json.dumps(arr)

   def list_client_meters(self, clt_dbid: int) -> str:
      arr = self.dbops.get_client_meters(clt_dbid)
      return json.dumps(arr)

   def read_redis(self, dbidx: int, keys: []) -> {}:
      def _strdic(d: {}) -> {}:
         x: {} = {}
         for k in d.keys():
            x[k.decode("utf-8")] = d[k].decode("utf-8")
         return x
      # -- -- --
      self.red.select(dbidx)
      d: {} = {}
      for k in keys:
         _dd: {} = self.red.hgetall(k)
         d[k] = _strdic(_dd)
      # -- -- -- --
      return d
