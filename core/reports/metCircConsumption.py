
from core.reports.kwhReading import kwhReading


class metCircConsumption(object):

   def __init__(self, rpt_jobid: int, y: int, m: int, fst: kwhReading, lst: kwhReading):
      self.rep_jobid = rpt_jobid
      self.rep_y: int = y
      self.rep_m: int = m
      self.fst: kwhReading = fst
      self.lst: kwhReading = lst
      self.monthly_kWhrs: float = 0.0
      self.error_code: int = 0
      self.error_msg: str = ""
      self._is_full_span: bool = \
         self.fst.is_fst_of_month() and self.lst.is_lst_of_month()
      self.met_circ_dbid: int = 0
      self.cir_tag: str = ""

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
      self.cir_tag = self.fst.cir_tag
      self.met_circ_dbid = self.lst.met_circ_id
      self.monthly_kWhrs = self.lst.calc_kWhrs(self.fst)
      if self.monthly_kWhrs is None or self.monthly_kWhrs < 0:
         print(f"MonthlyConsumptionLessThanZero: {self.monthly_kWhrs} / {self.cir_tag}")
         self.error_msg = "MonthlyConsumptionLessThanZero"
         self.error_code = 10
      # -- -- -- --
