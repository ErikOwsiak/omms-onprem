#!/usr/bin/env python3

import psycopg2

# host=localhost port=8787 dbname=sbms user=sbms_rest_api password=sbms_rest_api_pwd
host = "localhost"
# port = 5432
port = 8787
OMMS_DB_CONN = f"host={host} port={port} dbname=sbms user=sbms_rest_api password=sbms_rest_api_pwd"
print(f"\nOMMS_DB_CONN: {OMMS_DB_CONN}")


class ommsDB(object):

   def __init__(self, dbconn: str = None):
      self.dbconn = dbconn
      if self.dbconn is not None:
         global OMMS_DB_CONN
         OMMS_DB_CONN = self.dbconn

   def connect(self) -> bool:
      OPEN: int = 1
      self.dbconn = psycopg2.connect(OMMS_DB_CONN)
      if self.dbconn is not None and self.dbconn.status == OPEN:
         print("\tConnected")
         return True
      else:
         print("\tNotConnected")
         return False

   def dbconn(self):
      return self.dbconn

   def query(self, qry) -> ():
      cur = self.dbconn.cursor()
      cur.execute(qry)
      tmp = cur.fetchone()
      cur.close()
      return tmp

   def qry_1st_last(self, qry: str) -> []:
      cur = None
      try:
         arr_out = []
         cur = self.dbconn.cursor()
         cur.execute(qry)
         for rec in cur:
            arr_out.append(rec)
         return arr_out
      except Exception as e:
         print(e)
         return None
      finally:
         cur.close()

   def qry_arr(self, qry: str) -> []:
      cur = None
      try:
         arr_out = []
         cur = self.dbconn.cursor()
         cur.execute(qry)
         for rec in cur:
            arr_out.append(rec)
         return arr_out
      except Exception as e:
         print(e)
         return None
      finally:
         cur.close()

   def qry_val(self, qry: str) -> object:
      arr = self.qry_arr(qry)
      val = arr[0][0]
      return val

   def insert_1row(self, qry: str) -> [int, None]:
      cur = None
      try:
         cur = self.dbconn.cursor()
         cur.execute(qry)
         self.dbconn.commit()
         return cur.rowcount
      except Exception as e:
         print(e)
         return None
      finally:
         cur.close()
