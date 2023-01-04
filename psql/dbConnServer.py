
import psycopg2
from psycopg2.extensions import connection as _conn

CONN_STRING_FILE = "config/dbconn.string"


class dbConnServer(object):

   @staticmethod
   def getConnection() -> [_conn, None]:
      try:
         # ignore all lines with #
         with open(CONN_STRING_FILE, "r") as file:
            lines = file.readlines()
         lns = [x for x in lines if not x.startswith("#")]
         if lns[0] in (None, ""):
            raise Exception("BadDatabaseConnectionString")
         # - - - -
         connStr = lns[0].strip()
         conn: _conn = psycopg2.connect(connStr)
         if conn is None:
            raise Exception(f"UnableToConnect: {connStr}")
         if conn.info.status != 0:
            print(f"BadStatus: {conn.info.status}")
         return conn
      except Exception as e:
         print(e)
         return None
