
import datetime
from core.reports.kwhReading import kwhReading


class reportsSQL(object):

   @staticmethod
   def next_previous_reading(met_cir_dbid: int, dt: datetime.datetime):
      return f"""select * from streams.kwhs_raw t 
         where t.met_circ_dbid = {met_cir_dbid}
         and t.dts_utc < '{dt}' order by t.;"""

   @staticmethod
   def neighbourhood_reads(read: kwhReading, day_radius: int = 30):
      start_dt: datetime.date = read.dts_utc - datetime.timedelta(days=day_radius)
      end_dt: datetime.date = read.dts_utc + datetime.timedelta(days=day_radius)
      return f"""(select * from streams.kwhs_raw t where t.met_circ_dbid = {read.met_circ_id}
         and t.dts_utc > '{start_dt}' and t.dts_utc < '{end_dt}'
         order by t.dts_utc desc limit 1)
            union
      (select * from streams.kwhs_raw t where t.met_circ_dbid = {read.met_circ_id}
         and t.dts_utc > '{start_dt}' and t.dts_utc < '{end_dt}'
         order by t.dts_utc asc limit 1) order by dts_utc desc;"""

   @staticmethod
   def year_month_fst_read(met_cir_id: int, y: int, m: int):
      return f"select * from streams.kwhs_raw t where t.met_circ_dbid = {met_cir_id}" \
         f" and extract(year from cast(t.dts_utc as date))::int = {y}" \
         f" and extract(month from cast(t.dts_utc as date))::int = {m}" \
         f" order by t.dts_utc asc limit 1;"

   @staticmethod
   def year_month_lst_read(met_cir_id: int, y: int, m: int):
      return f"select * from streams.kwhs_raw t where t.met_circ_dbid = {met_cir_id}" \
         f" and extract(year from cast(t.dts_utc as date))::int = {y}" \
         f" and extract(month from cast(t.dts_utc as date))::int = {m}" \
         f" order by t.dts_utc desc limit 1;"

   @staticmethod
   def backfill_kwhrs(met_cir_id: int, tl_kwh: float, dtsutc: str):
      tbl = "streams.kwhs_raw"
      return f"insert into {tbl} (met_circ_dbid, dts_utc, is_backfilled," \
         f" total_kwhs, l1_kwhs, l2_kwhs, l3_kwhs, backfill_notes)" \
         f" values({met_cir_id}, '{dtsutc}', true, {tl_kwh}, null, null, null, 'backfill')" \
         f" returning row_dbid;"
