import gc

from psycopg2.extensions import connection
from psycopg2.extensions import cursor
from core.logProxy import logProxy


class dbOps(object):

   NULL = 'null'
   PWR_STATS_TBL = "streams.power_stats"

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
      # -- -- -- --
      ins = f"insert into streams.kwhs_raw" \
         f" values(default, {dbid}, now(), {tkwhs}, {l1kwhs}, {l2kwhs}, {l3kwhs}) returning row_dbid;"
      cur: cursor = self.conn.cursor()
      cur.execute(ins)
      self.conn.commit()
      rowcount = cur.rowcount
      cur.close()
      return rowcount == 1

   def insert_elect_kwhrs_dict(self, dbid: int, _dict: {}) -> bool:
      cur: cursor = None
      try:
         tl_kwh = _dict["tl_kwh"] if "tl_kwh" in _dict.keys() else dbOps.NULL
         l1_kwh = _dict["l1_kwh"] if "l1_kwh" in _dict.keys() else dbOps.NULL
         l2_kwh = _dict["l2_kwh"] if "l2_kwh" in _dict.keys() else dbOps.NULL
         l3_kwh = _dict["l3_kwh"] if "l3_kwh" in _dict.keys() else dbOps.NULL
         ins = f"insert into streams.kwhs_raw" \
            f" values(default, {dbid}, now(), {tl_kwh}, {l1_kwh}, {l2_kwh}, {l3_kwh}) returning row_dbid;"
         cur = self.conn.cursor()
         cur.execute(ins)
         self.conn.commit()
         return cur.rowcount == 1
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()

   def insert_elect_pwr_stats(self, dbid: int, _dict: {}):
      cur: cursor = None
      try:
         # -- misc --
         ghz = _dict["grid_hz"] if "grid_hz" in _dict.keys() else dbOps.NULL
         # -- volts --
         lnv = _dict["ln_v"] if "ln_v" in _dict.keys() else dbOps.NULL
         l1v = _dict["l1_v"] if "l1_v" in _dict.keys() else dbOps.NULL
         l2v = _dict["l2_v"] if "l2_v" in _dict.keys() else dbOps.NULL
         l3v = _dict["l3_v"] if "l3_v" in _dict.keys() else dbOps.NULL
         # -- amps --
         tla = _dict["tl_a"] if "tl_a" in _dict.keys() else dbOps.NULL
         l1a = _dict["l1_a"] if "l1_a" in _dict.keys() else dbOps.NULL
         l2a = _dict["l2_a"] if "l2_a" in _dict.keys() else dbOps.NULL
         l3a = _dict["l3_a"] if "l3_a" in _dict.keys() else dbOps.NULL
         # -- watts --
         tlw = _dict["tl_w"] if "tl_w" in _dict.keys() else dbOps.NULL
         l1w = _dict["l1_w"] if "l1_w" in _dict.keys() else dbOps.NULL
         l2w = _dict["l2_w"] if "l2_w" in _dict.keys() else dbOps.NULL
         l3w = _dict["l3_w"] if "l3_w" in _dict.keys() else dbOps.NULL
         # -- power factor --
         tlpf = _dict["tl_pf"] if "tl_pf" in _dict.keys() else dbOps.NULL
         l1pf = _dict["l1_pf"] if "l1_pf" in _dict.keys() else dbOps.NULL
         l2pf = _dict["l2_pf"] if "l2_pf" in _dict.keys() else dbOps.NULL
         l3pf = _dict["l3_pf"] if "l3_pf" in _dict.keys() else dbOps.NULL
         # -- build insert --
         ins = f"insert into {dbOps.PWR_STATS_TBL} values(default, {dbid}, now(), {ghz}," \
            f" {lnv}, {l1v}, {l2v}, {l3v}, {tla}, {l1a}, {l2a}, {l3a}," \
            f" {tlw}, {l1w}, {l2w}, {l3w}, {tlpf}, {l1pf}, {l2pf}, {l3pf}) returning row_dbid;"
         print(ins)
         # -- insert --
         cur: cursor = self.conn.cursor()
         cur.execute(ins)
         self.conn.commit()
         return cur.rowcount == 1
      except Exception as e:
         logProxy.log_exp(e)
      finally:
         cur.close()
