
import datetime


class sysCircuitInfo(object):

   def __init__(self, r: []):
      # -- -- -- --
      self.met_circ_id: int = int(r[0])
      self.cir_tag: str = r[1]
      self.spath: str = r[2]
      self.elcrm: str = r[3]
      self.met_dt_crd: datetime.datetime = r[4]


class reportData(object):

   def __init__(self, cir_tag: str, kwhrs: int, s_read: str, e_read: str):
      self.cir_tag: str = cir_tag
      self.kwhrs: int = kwhrs
      self.s_read: str = s_read
      self.e_read: str = e_read


class clientReport(object):

   def __init__(self, clt_dbid: int
         , rpt_jobid: int
         , clt_tag: str
         , clt_name: str
         , year: int
         , month: int
         , kwh: float
         , note: str):
      # -- -- -- --
      self.clt_dbid: int = clt_dbid
      self.clt_tag: str = clt_tag
      self.clt_name: str = clt_name
      self.rpt_jobid: int = rpt_jobid
      self.year: int = year
      self.month: int = month
      self.kwh: float = kwh
      self.note: str = note
