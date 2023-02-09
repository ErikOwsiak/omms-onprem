
from core.reports.kwhReading import kwhReading
from core.reports.reportsDatatypes import sysCircuitInfo


class metCircConsumption(object):

   def __init__(self, rpt_jobid: int
         , y: int
         , m: int
         , sys_circ: sysCircuitInfo
         , fst: kwhReading
         , lst: kwhReading):
      # -- -- -- -- -- -- -- --
      self.rep_jobid = rpt_jobid
      self.rep_y: int = y
      self.rep_m: int = m
      self.sys_circ: sysCircuitInfo = sys_circ
      self.fst: kwhReading = fst
      self.lst: kwhReading = lst
      self.monthly_kWhrs: float = 0.0
      self.error_code: int = 0
      self.error_msg: str = ""
      self._is_full_span: bool = \
         self.fst.is_fst_of_month() and self.lst.is_lst_of_month()
      self.met_circ_dbid: int = 0

   @property
   def is_full_span(self) -> bool:
      return self._is_full_span

   def update_monthly_consumption(self):
      # -- -- -- --
      if self.fst.met_circ_id != self.lst.met_circ_id:
         raise Exception("BadData[met_circ_id]")
      if self.fst.cir_tag != self.lst.cir_tag:
         raise Exception("BadData[cir_tag]")
      # -- -- -- --
      self.monthly_kWhrs = self.lst.calc_kWhrs(self.fst)
      if self.monthly_kWhrs is None or self.monthly_kWhrs < 0:
         self.error_msg = "MonthlyConsumptionLessThanZero"
         print(f"{self.error_msg}:")
         print(f"\t{self.monthly_kWhrs} | {self.sys_circ.cir_tag} | {self.sys_circ.spath}")
         self.error_code = 10
      # -- -- -- --
