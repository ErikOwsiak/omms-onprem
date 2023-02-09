
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
