
import psycopg2
from psycopg2.extensions import connection as _psql_conn


class dbConnServer(object):

   @staticmethod
   def getConnection(connStr: str) -> [_psql_conn, None]:
      try:
         conn: _psql_conn = psycopg2.connect(connStr)
         if conn is None:
            raise Exception(f"UnableToConnect: {connStr}")
         if conn.info.status != 0:
            print(f"BadStatus: {conn.info.status}")
         return conn
      except Exception as e:
         print(e)
         return None
