import enum

import psycopg2, json
from psycopg2.extensions import cursor, connection as _psql_conn
from flask import request
from webui.api.dbEditSql import dbEditSql
from psql.dbConnServer import dbConnServer


class bitflags(enum.Enum):
   DEL = 0xff


class dbEdit(object):

   def __init__(self, conn_str: str, action: str, req: request):
      self.conn_str = conn_str
      self.action: str = action
      self.req: request = req
      self.conn = None
      # -- data out --
      self.buffout_ctype: str = "text/json"
      self.buffout_error: int = 200
      self.buffout: str = ""

   def __del__(self):
      try:
         if self.conn is not None:
            self.conn.close()
            self.conn = None
      finally:
         pass

   def run_action(self) -> int:
      # -- -- -- --
      self.conn: _psql_conn = dbConnServer.getConnection(self.conn_str)
      act: str = self.action.replace("/", "_")
      method_name = f"_{act}"
      has_method = hasattr(self, method_name)
      # -- -- -- --
      if has_method:
         _method = getattr(self, method_name)
         method_error: int = _method()
         if method_error != 0:
            pass
         else:
            pass
      else:
         pass
      # -- -- -- --
      return 0

   def _get_table_info(self) -> int:
      self.req: request = self.req
      tblname: str = self.req.args["tbl"]
      sql = dbEditSql.table_info(tblname)
      cur: cursor = self.conn.cursor()
      cur.execute(sql)
      row = cur.fetchone()
      if row is None:
         self.buffout = ""
         self.buffout_error = 404
      else:
         self.buffout = row[0]
         self.buffout_error = 200
      return 0

   def _get_clients(self):
      qry = dbEditSql.all_clients()
      return self.__select_qry_rows(qry)

   def _get_client_circuits(self):
      qry = dbEditSql.client_circuits()
      return self.__select_qry_rows(qry)

   def _get_elec_meter_circuits(self):
      qry = dbEditSql.elec_meter_circuits()
      return self.__select_qry_rows(qry)

   def _get_datalists(self):
      """
         1. locate available circuits
            a. look for cir_tags in core.elec_meter_circuits that are not in config.client_circuits
            2. look for cir_tags in config.client_circuits where dt_link & dt_unlink not null
      """
      cur: cursor = self.conn.cursor()
      try:
         iso_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED
         self.conn.set_session(isolation_level=iso_level, readonly=True, autocommit=True)
         # -- clients --
         qry_clts = "select t.clt_rowid, t.clt_tag, t.clt_name from config.clients t;"
         cur.execute(qry_clts)
         clts_rows = cur.fetchall()
         # -- meter circuits; only those not linked to clients; --
         # qry_cirs = """select t.met_cir_rowid, t.cir_tag
         #    from core.elec_meter_circuits t where t.cir_tag in
         #    (select cc.cir_tag from config.client_circuits cc where cc.clt_tag is null);"""
         qry_cirs = dbEditSql.available_circuits()
         cur.execute(qry_cirs)
         cirs_rows = cur.fetchall()
         # -- building locales --
         qry_locls = "select t.locl_rowid, t.bld_tag, t.locl_tag from core.bld_locales t;"
         cur.execute(qry_locls)
         locls_rows = cur.fetchall()
         d: {} = {"clts": clts_rows, "cirs": cirs_rows, "locs": locls_rows}
         self.buffout = json.dumps(d)
         self.buffout_error = 200
         return 0
      except Exception as e:
         print(e)
      finally:
         cur.close()

   def _upsert(self) -> int:
      # -- upsert table --
      d: {} = {"EditorAction": "Upsert"}
      tblname: str = self.req.args["tbl"]
      if tblname == "clients":
         qry = dbEditSql.upsert_clients(self.req.values)
      elif tblname == "client_circuits":
         qry = dbEditSql.upsert_client_circuits(self.req.values)
      else:
         d["Error"] = "BadTableName"
         self.buffout = json.dumps(d)
         self.buffout_error = 588
         return 1
      # -- -- -- --
      cur: cursor = self.conn.cursor()
      try:
         cur.execute(qry)
         row, = cur.fetchone()
         if row is None:
            d["ErrorMsg"] = "RowIsNone"
            self.buffout = json.dumps(d)
            self.buffout_error = 404
            self.conn.rollback()
         else:
            d["ErrorMsg"] = "OK"; d["ReturnedRowID"] = row
            self.buffout = json.dumps(d)
            self.buffout_error = 200
         return 0
      except Exception as e:
         print(e)
      finally:
         self.conn.commit()
         cur.close()

   def _delete(self):
      # -- -- -- --
      qry = ""
      d: {} = {"EditorAction": "Delete"}
      # -- -- -- --
      try:
         tblname: str = self.req.args["tbl"]
         rowid = self.req.values["rowid"]
         if tblname == "clients":
            qry = f"update config.clients set bitflags = (bitflags + {bitflags.DEL.value})" \
               f", dt_del = now() where clt_rowid = {rowid};"
         elif tblname == "client_circuits":
            bitflag = bitflags.DEL.value
            qry = f"update config.client_circuits set bitflags = (bitflags + {bitflag})" \
               f", dt_unlink = now() where row_sid = {rowid};"
         else:
            d["ErrorMsg"] = "BadTableName"
            self.buffout = json.dumps(d)
            self.buffout_error = 588
            return 1
      except Exception as e:
         print(e)
      # -- -- -- --
      cur: cursor = self.conn.cursor()
      try:
         cur.execute(qry)
         if cur.rowcount == 1:
            d["ErrorMsg"] = "OK"
            self.buffout = json.dumps(d)
            self.buffout_error = 200
         else:
            self.buffout = ""
            self.buffout_error = 404
            self.conn.rollback()
         return 0
      except Exception as e:
         print(e)
      finally:
         self.conn.commit()
         cur.close()

   # def _del_client(self, rowid: int):
   #    qry = f"update config.clients set bitflags = (bitflags + {bitflags.DEL.value})" \
   #       f", dt_del = now() where clt_rowid = {rowid};"
   #    cur: cursor = self.conn.cursor()
   #    try:
   #       cur.execute(qry)
   #       if cur.rowcount == 1:
   #          self.conn.commit()
   #    except Exception as e:
   #       print(e)
   #    finally:
   #       cur.close()

   def __qry_rows(self, qry: str):
      cur: cursor = self.conn.cursor()
      try:
         iso_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED
         self.conn.set_session(isolation_level=iso_level, readonly=True, autocommit=True)
         cur.execute(qry)
         rows = cur.fetchall()
         if rows is None:
            self.buffout = json.dumps({"Rows": 0})
            self.buffout_error = 404
         else:
            self.buffout = json.dumps(rows)
            self.buffout_error = 200
         return 0
      except Exception as e:
         self.buffout = json.dumps({"Exception": str(e)})
         self.buffout_error = 556
      finally:
         cur.close()

   def __select_qry_rows(self, qry):
      cur: cursor = self.conn.cursor()
      try:
         iso_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED
         self.conn.set_session(isolation_level=iso_level, readonly=True, autocommit=True)
         cur.execute(qry)
         rows = cur.fetchall()
         if rows is None:
            self.buffout = json.dumps({"Rows": 0})
            self.buffout_error = 404
         else:
            self.buffout = json.dumps(rows)
            self.buffout_error = 200
         return 0
      except Exception as e:
         self.buffout = json.dumps({"Exception": str(e)})
         self.buffout_error = 556
      finally:
         cur.close()
