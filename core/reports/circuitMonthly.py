
import datetime, calendar as cal
from core.reports.backFiller import backFiller
# from core.ommsdb import ommsDB
from core.utils import sysUtils as utils


class circuitMonthly(object):

   ERR_BACK_FILL = "UNABLE_TO_BACK_FILL"

   def __init__(self, db, dbid: int, cirtag: str, year: int, months: []):
      self.db = db
      self.meter_dbid = dbid
      self.cirtag = cirtag
      self.year = year
      self.months: [] = months
      self.runid = None
      self.tbl = "kwhrs_v2"

   def init(self):
      pass

   def run(self, **kwargs):
      self.runid = kwargs["runid"]
      for m in self.months:
         rval = self.__for_month(self.year, m)
         print(f"\n\t-- [ METER Monthly: {self.meter_dbid} | {self.cirtag} | {self.year}/{m} | rval: {rval} ]")
         if rval.startswith("-") and float(rval) < 0:
            print("= = = = = = = = = = = = = = = = = = = = = =\n")

   def __for_month(self, y: int, m: int) -> str:
      try:
         # get month's 1st reading & try backfill on missing
         if self.meter_dbid == 1013:
            print("got trap")
         s_tup_out = self.__fst_reading(y, m)
         if s_tup_out is None:
            return f"{circuitMonthly.ERR_BACK_FILL}_FST"
         # get month's last reading & try backfill on missing
         e_tup_out = self.__lst_reading(y, m)
         if e_tup_out is None:
            return f"{circuitMonthly.ERR_BACK_FILL}_LST"
         # -- load data --
         # t.row_id, t.fk_meter_dbid, t.reading_dts_utc, t.total_kwhrs
         s_pk, s_dbid, s_dts, s_kwh = s_tup_out
         e_pk, e_dbid, e_dts, e_kwh = e_tup_out
         if s_dbid != e_dbid:
            # -- error --
            dts_now = utils.dts_now()
            self.__ins_qry(self.meter_dbid, y, m, 1, "BAD_DBIDS", 0, dts_now, 0, dts_now, 0)
            return "BAD_DBIDS"
         # -- do --
         diff_kwh: float = e_kwh - s_kwh
         # -- ins good row --
         self.__ins_qry(self.meter_dbid, y, m, 0, "", s_kwh, s_dts, e_kwh, e_dts, diff_kwh)
         # this should not ever happen
         if diff_kwh <= 0:
            print("\n\n-------------------------------------------------")
            print(["star reading", s_pk, s_dbid, float(s_kwh), str(s_dts)])
            print(["end reading", e_pk, e_dbid, float(e_kwh), str(e_dts)])
         # -- return kwhrs --
         return f"{diff_kwh}"
      except Exception as e:
         print(e)
      finally:
         pass

   def __read_top_row(self, rd: datetime.date, fst_lst: str) -> ():
      # -- map order by to get first or last row --
      if fst_lst not in ("fst", "lst"):
         raise Exception(f"BadFstLst: {fst_lst}")
      # -- run --
      _dir = {"fst": "asc", "lst": "desc"}[fst_lst]
      sdate = f"{rd.year}-{rd.month:02d}-{rd.day:02d}"
      edate = utils.next_month_day_str(rd.year, rd.month)
      # -- return qry --
      # t.fk_meter_dbid, t.reading_dts_utc, t.total_kwhrs
      qry = f"select t.row_id, t.fk_meter_dbid, t.reading_dts_utc, t.total_kwhrs" \
         f" from streams.{self.tbl} t where t.fk_meter_dbid = {self.meter_dbid}" \
         f" and t.reading_dts_utc >= '{sdate}' and t.reading_dts_utc < '{edate}'" \
         f" order by t.reading_dts_utc {_dir} limit 1;"
      rval: () = self.db.query(qry)
      if rval is None or len(rval) == 0:
         return None
      else:
         return rval

   def __fst_reading(self, y: int, m: int) -> [(), None]:
      read_date: datetime.date = datetime.date(y, m, 1)
      tup_out = self.__read_top_row(read_date, "fst")
      if tup_out is not None:
         return tup_out
      # -- try backfill --
      bf: backFiller = backFiller(self.db, self.tbl, self.meter_dbid)
      if bf.backfill_fst_of_month(read_date):
         tup_out = self.__read_top_row(read_date, "fst")
      else:
         dts_now = utils.dts_now()
         EMSG = f"{circuitMonthly.ERR_BACK_FILL}_FST"
         self.__ins_qry(self.meter_dbid, y, m, 1, EMSG, 0, dts_now, 0, dts_now, 0)
         return None
      # -- return --
      return tup_out

   def __lst_reading(self, y: int, m: int) -> [(), None]:
      _, day_idx = cal.monthrange(y, m)
      read_date: datetime.date = datetime.date(y, m, day_idx)
      tup_out = self.__read_top_row(read_date, "lst")
      if tup_out is not None:
         return tup_out
      # -- try backfill --
      bf: backFiller = backFiller(self.db, self.tbl, self.meter_dbid)
      if bf.backfill_lst_of_month(read_date):
         tup_out = self.__read_top_row(read_date, "lst")
      else:
         dts_now = utils.dts_now()
         EMSG = f"{circuitMonthly.ERR_BACK_FILL}_LST"
         self.__ins_qry(self.meter_dbid, y, m, 1, EMSG, 0, dts_now, 0, dts_now, 0)
         return None
      # -- return --
      return tup_out

   # = = = = = = = = = = insert query string  = = = = = = = = = = = =
   def __ins_qry(self, dbid: int, y: int, m: int, err: int, errmsg: str
         , skwh: float, sdts: str, ekwh: float, edts: str, kwhdiff: float):
      try:
         qry: str = f"insert into reports.elec_meter_monthly" \
            f" values(default, {dbid}, '{self.runid}', {err}, '{errmsg}', {y}, {m}," \
            f" {skwh}, '{sdts}', {ekwh}, '{edts}', {kwhdiff}, now());"
         # -- run query --
         if self.db.insert_1row(qry) == 1:
            print("\t  + monthly report inserted")
         else:
            print("\t  - monthly report NOT inserted")
      except Exception as _e:
         print(_e)
      finally:
         pass
