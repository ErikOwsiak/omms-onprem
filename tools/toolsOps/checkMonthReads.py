
import sys, datetime
# -- system --
from psql.dbOps import dbOps
from core.datatypes import sysCircuit
from tools.toolsOps.sqlCode import sqlCode
from tools.toolsOps.readFixer import readFixer
from core.reports.kwhReading import kwhReading


class monthReadsChecker(object):

   def __init__(self, month: int, year: int, dbconn: str):
      self.month: int = month
      self.year: int = year
      self.dbconn: str = dbconn
      self.dbops: dbOps = dbOps(dbconn)
      self.circuits: [] = None

   def run(self) -> int:
      try:
         if self.__load_circuits() == 0:
            print("NoSystemCircuits")
            sys.exit(1)
         # -- --
         [self.__process_circuit(c) for c in self.circuits]
         return 0
      except Exception as e:
         print(e)

   def __load_circuits(self) -> int:
      arr: [] = self.dbops.get_system_circuits()
      if len(arr) == 0:
         print("NoSystemCircuitsDbFound")
         sys.exit(1)
      # -- --
      self.circuits = []
      [self.circuits.append(sysCircuit(i)) for i in arr]
      return len(self.circuits)

   def __process_circuit(self, cir: sysCircuit):
      sql: str = sqlCode.check_circuit_readings(m=self.month, y=self.year, cirid=cir.met_cir_rowid)
      arr: [] = self.dbops.qry_to_rows(sql)
      cnt: int = len(arr)
      if cnt == 0:
         msg = f"[ met_cir_dbid: {cir.met_cir_rowid} | cirtag: {cir.cir_tag} | no data ]"
         self.__try_fix_month(cir)
      else:
         dtsF: datetime.datetime = arr[0][2]; valF = round(float(arr[0][4]), 2)
         dtsN: datetime.datetime = arr[-1][2]; valN = round(float(arr[-1][4]), 2)
         msg = f"[ met_cir_dbid: {cir.met_cir_rowid} | cirtag: {cir.cir_tag} | rows: {cnt} ]" \
            f"\n\tfst -> {dtsF.replace(microsecond=0)} | {valF} kWh" \
            f"\n\tlst -> {dtsN.replace(microsecond=0)} | {valN} kWh" \
            f"\n"
      # -- --
      print(msg)

   def __try_fix_month(self, cir: sysCircuit):
      try:
         fixer: readFixer = readFixer(self.dbops, cir, self.year, self.month)
         prv_kwh, nxt_kwh = fixer.pull_data()
         # -- --
         prv_kwh: kwhReading = prv_kwh
         nxt_kwh: kwhReading = nxt_kwh
         # -- --
         fixer.fix_data(prv_kwh, nxt_kwh)
         # -- --
      except Exception as e:
         print(e)
