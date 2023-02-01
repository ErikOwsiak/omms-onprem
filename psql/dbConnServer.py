
import psycopg2
from psycopg2.extensions import connection as _psql_conn
from core.logProxy import logProxy


class dbConnServer(object):

   @staticmethod
   def getConnection(connStr: str, readonly: bool = False) -> [_psql_conn, None]:
      try:
         conn: _psql_conn = psycopg2.connect(connStr)
         if conn is None:
            raise Exception(f"UnableToConnect: {connStr}")
         if conn.info.status != 0:
            print(f"BadStatus: {conn.info.status}")
         # -- as readonly; so lookups --
         if readonly:
            iso_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED
            conn.set_session(isolation_level=iso_level, readonly=True, autocommit=True)
         # -- return connection object --
         return conn
      except Exception as e:
         logProxy.log_exp(e)
         return None
