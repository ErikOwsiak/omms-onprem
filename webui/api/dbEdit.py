
import json

import psycopg2
from psycopg2.extensions import connection as _psql_conn
from psycopg2.extensions import cursor
from flask import request
from webui.api.dbEditSql import dbEditSql


class dbEdit(object):

   def __init__(self, conn: _psql_conn, action: str, req: request):
      self.conn = conn
      self.action: str = action
      self.req: request = req
      # -- data out --
      self.buffout_ctype: str = "text/json"
      self.buffout_error: int = 200
      self.buffout: str = ""

   def run_action(self) -> int:
      # -- -- -- --
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
      qry = dbEditSql.get_clients()
      return self.__select_qry_rows(qry)

   def _get_client_meter_circuits(self):
      qry = dbEditSql.clt_met_cirs_rows()
      return self.__select_qry_rows(qry)

   def _get_elec_meter_circuits(self):
      qry = dbEditSql.elec_meter_circuits()
      return self.__select_qry_rows(qry)

   def _upsert(self) -> int:
      # -- upsert table --
      d: {} = {"EditorAction": "Upsert"}
      tblname: str = self.req.args["tbl"]
      if tblname == "clients":
         qry = dbEditSql.upsert_clients(self.req.values)
      elif tblname == "client_meter_circuits":
         qry = dbEditSql.upsert_client_meter_circuits(self.req.values)
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
      # -- upsert table --
      d: {} = {"EditorAction": "Delete"}
      tblname: str = self.req.args["tbl"]
      rowid = self.req.values["rowid"]
      if tblname == "clients":
         qry = f"delete from config.clients where clt_rowid = {rowid};"
      elif tblname == "client_meter_circuits":
         qry = f"delete from config.clients where clt_rowid = {rowid};"
      else:
         d["ErrorMsg"] = "BadTableName"
         self.buffout = json.dumps(d)
         self.buffout_error = 588
         return 1
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

   def __select_qry_rows(self, qry):
      # -- -- -- -- -- -- -- --
      cur: cursor = self.conn.cursor()
      try:
         iso_level = psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED
         self.conn.set_session(isolation_level=iso_level, readonly=True, autocommit=True)
      except Exception as e:
         print(e)
      # -- -- -- -- -- -- -- --
      try:
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
