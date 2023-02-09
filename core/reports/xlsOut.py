
import xlsxwriter as xw
import os.path, configparser as _cp
from xlsxwriter.workbook import Worksheet
from psql.dbOps import dbOps
from core.utils import sysUtils as utils
from core.logProxy import logProxy

"""
   https://xlsxwriter.readthedocs.io/worksheet.html
"""

class xlsOut(object):

   def __init__(self, ini: _cp.ConfigParser
         , dbops: dbOps
         , rpt_jobid: int
         , y: int
         , m: int):
      # -- -- -- --
      self.ini: _cp.ConfigParser = ini
      self.dbops: dbOps = dbops
      self.rpt_jobid: int = rpt_jobid
      self.yr: int = y
      self.mn: int = m
      self.wb: xw.workbook = None
      self.rpt_path: str = ""
      self.rpt_prefix: str = ""
      self.xlsx_file: str = ""

   def init(self) -> int:
      self.rpt_path = self.ini.get("BACKEND", "REPORTS_PATH")
      if not os.path.exists(self.rpt_path):
         return 1
      self.rpt_prefix = self.ini.get("BACKEND", "XLSX_PREFIX")
      self.rpt_prefix = self.rpt_path if self.rpt_path in ["", None] else "kwhrs"
      self.xlsx_file = f"{self.rpt_prefix}_{self.yr}_{self.mn:02d}_({self.rpt_jobid}).xlsx"
      print([self.rpt_path, self.xlsx_file])

   def create(self):
      # -- -- -- --
      rpt_arr: [] = self.dbops.get_rpt_job_data(self.rpt_jobid)
      if rpt_arr is None:
         print(f"NoDataFoundForJobID: {self.rpt_jobid}")
         return
      # -- -- -- --
      xlsx_path = f"{self.rpt_path}/{self.yr}/{self.xlsx_file}"
      self.wb: xw.workbook = xw.Workbook(xlsx_path)
      wsh_ri = self.wb.add_worksheet("Report_Info")
      rp: {} = {"DatetimeUTC": utils.dts_utc()
         , "ReportJobID": self.rpt_jobid
         , "ReportType": "kwhrs"}
      if not self.__fill_report_info(rp, wsh_ri):
         pass
      # -- -- -- --
      wsh_cl = self.wb.add_worksheet("Client_kWhrs")
      if not self.__fill_client_kwhrs(rpt_arr, self.yr, self.mn, wsh_cl):
         pass
      # -- -- -- --
      wsh_mt = self.wb.add_worksheet("Circuit_kWhrs")
      if not self.__fill_circuit_kwhrs(rpt_arr, wsh_mt):
         pass
      # -- -- -- --
      wsh_lp = self.wb.add_worksheet("Lookup_Info")
      if not self.__fill_lookup_info(wsh_lp):
         pass
      # -- -- -- --
      if self.__backup_prev_xlsx(self.yr, self.mn):
         self.wb.close()
      else:
         pass
      # -- -- -- --

   def __backup_prev_xlsx(self, y: int, m: int) -> bool:
      path: str = f"{self.rpt_path}/{y}"
      files = os.listdir(path)
      for file in files:
         try:
            if f"_{m:02d}_" not in file:
               continue
            old, new = f"{path}/{file}", f"{self.rpt_path}/backup/{file}"
            os.rename(old, new)
         except Exception as e:
            logProxy.log_exp(e)
            continue
      # -- for now let it be --
      return True

   """
      # -- col names;  write(row, col, *args) --
   """
   def __fill_report_info(self, _dict: {}, wsh: Worksheet) -> bool:
      # -- -- -- --
      dct = {"bold": False, "font_color": "#25165C", "font_size": 12}
      frmtKey = self.wb.add_format(dct)
      dct = {"bold": False, "font_color": "#4d495E", "font_size": 12}
      frmtVal = self.wb.add_format(dct)
      # -- -- -- --
      row: int = 1; key_col: int = 1; val_col: int = 2
      key_col_w: int = 0; val_col_w: int = 0
      # -- -- -- --
      def __add(key, val):
         nonlocal row, key_col_w, val_col_w
         row += 1
         # -- key --
         key_cal_w = key_col_w if key_col_w > len(key) else (len(key) + 12)
         wsh.set_column(row, key_col, key_cal_w)
         wsh.write(row, key_col, key, frmtKey)
         # -- val --
         val_col_w = val_col_w if val_col_w > len(val) else (len(val) + 12)
         wsh.set_column(row, val_col, val_col_w)
         wsh.write(row, val_col, val, frmtVal)
      # -- -- -- --
      fntclr = ""
      dct = {"bold": True, "font_color": f"{fntclr}", "font_size": 14}
      frmtHdr = self.wb.add_format(dct)
      wsh.write(row, key_col, "Key", frmtHdr)
      wsh.write(row, val_col, "Value", frmtHdr)
      row += 1
      # -- -- -- --
      for item in _dict.items():
         k, v = item
         __add(k, str(v))
      return True

   def __fill_lookup_info(self, wsh: Worksheet) -> bool:
      # - - - - - -
      row_idx = 0
      wsh.set_column(0, 0, 16)
      wsh.write(row_idx, 0, "NIP | Client")
      wsh.write(row_idx, 1, "space_tag")
      wsh.set_column(2, 2, 16)
      wsh.write(row_idx, 2, "circuit_tag")
      # --- fill ---
      """ c.clt_name
         , t.clt_tag
         , t.locl_tag
         , t.cir_tag"""
      clt_cirs = self.dbops.get_clients_circuits()
      col0_w: int = 0
      for tup in clt_cirs:
         row_idx += 1
         clt, nip, ltag, ctag = tup
         tagclt = f"{nip} | {clt}"
         wsh.write(row_idx, 0, tagclt)
         col0_w = col0_w if col0_w > len(tagclt) else (len(tagclt) + 10)
         wsh.set_column(1, 1, col0_w)
         wsh.write(row_idx, 1, ltag)
         wsh.write(row_idx, 2, ctag)
      return True

   def __fill_circuit_kwhrs(self, arr_tups: []
         , wsh: Worksheet) -> bool:
      # -- -- -- --
      dct = {"bold": True, "font_color": "#091378", "font_size": 12}
      bold_cell = self.wb.add_format(dct)
      # -- load data --
      col0_w: int = 0; row_idx: int = 0
      for tup in arr_tups:
         row_idx += 1
         _, _, _, _, nip, clt, y, m, _, buff, _ = tup
         wsh.write(row_idx, 0, "")
         row_idx += 1
         tag_cld = f"{nip} | {clt}"
         col0_w = col0_w if col0_w > len(tag_cld) else (len(tag_cld) + 8)
         wsh.set_column(0, 0, col0_w)
         wsh.write(row_idx, 0, tag_cld, bold_cell)
         # -- for each calc --
         calcs_rows: [] = [s.strip() for s in buff.split("&&")]
         for c in calcs_rows:
            try:
               fst, lst = [s.strip() for s in c.strip().split("|")]
               cir, kwh, dts = [s.strip() for s in lst.strip().split(";")]
               msg: str = f"        {cir} | {kwh} kwh | {dts} UTC"
               row_idx += 1
               wsh.write(row_idx, 0, msg)
            except Exception as e:
               logProxy.log_exp(e)
      # -- the end --
      return True

   def __fill_client_kwhrs(self, arr_arr: []
         , y: int
         , m: int
         , wsh_totals: Worksheet) -> bool:
      # -- col names --
      row: int = 0
      wsh_totals.write(row, 0, "NIP")
      wsh_totals.write(row, 1, "ClientName")
      wsh_totals.write(row, 2, f"{y}_{m}_kWh")
      row += 2
      # -- cell format --
      fnt_color = "#800000"
      dct = {"bold": True, "font_color": f"{fnt_color}", "font_size": 12}
      clt_frmt = self.wb.add_format(dct)
      # -- load data --
      col0_w, col1_w = 0, 0
      for arr in arr_arr:
         ctag, cname, _, _, kwh = arr[4:9]
         print(f"\txls_write: {ctag} | {cname} | {kwh}")
         y = int(y); m = int(m); kwh = float(kwh)
         col0_w = col0_w if col0_w > len(ctag) else (len(ctag) + 10)
         wsh_totals.set_column(0, 0, col0_w)
         wsh_totals.write(row, 0, ctag)
         # -- col width --
         col1_w = col1_w if col1_w > len(cname) else (len(cname) + 10)
         wsh_totals.set_column(1, 1, col1_w)
         wsh_totals.write(row, 1, cname, clt_frmt)
         # -- -- -- -- -- --
         # -- date: yr-mn --
         wsh_totals.set_column(2, 2, 16)
         wsh_totals.write(row, 2, round(float(kwh), 2))
         row += 1
      # -- the end --
      return True
