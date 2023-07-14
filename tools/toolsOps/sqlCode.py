

class sqlCode(object):

   @staticmethod
   def check_circuit_readings(m: int, y: int, cirid: int):
      tbl = "streams.kwhs_raw"
      return f"select * from {tbl} t where t.met_circ_dbid = {cirid}" \
         f" and extract(year from t.dts_utc) = {y}" \
         f" and extract(month from t.dts_utc) = {m}" \
         f" order by t.dts_utc asc;"
