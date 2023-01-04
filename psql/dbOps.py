
from psycopg2.extensions import connection
from psycopg2.extensions import cursor


class dbOps(object):

   def __init__(self, conn: connection):
      self.conn: connection = conn

   def get_meter_syspath_dbid(self, syspath: str) -> int:
      cur: cursor = self.conn.cursor()
      try:
         qry = f"select t.met_dbid from config.meters t where t.syspath = '{syspath}';"
         cur.execute(qry)
         row = cur.fetchone()
         if row is not None:
            return int(row[0])
         else:
            qry = f"insert into config.meters" \
               f" values(default, '{syspath}', 'Unknown', 'Unknown', 'Unknown', now()) returning met_dbid;"
            cur.execute(qry)
            row = cur.fetchone()
            self.conn.commit()
            if cur.rowcount == 1:
               dbid: int = row[0]
               return dbid
            else:
               pass
      except Exception as e:
         print(e)
      finally:
         cur.close()

   def insert_elect_kwhrs(self, dbid: int, tkwhs: float, l1kwhs, l2kwhs, l3kwhs) -> bool:
      # -- run --
      ins = f"insert into streams.kwhs_raw" \
         f" values(default, {dbid}, now(), {tkwhs}, {l1kwhs}, {l2kwhs}, {l3kwhs}) returning row_dbid;"
      cur: cursor = self.conn.cursor()
      cur.execute(ins)
      self.conn.commit()
      rowcount = cur.rowcount
      cur.close()
      return rowcount == 1
