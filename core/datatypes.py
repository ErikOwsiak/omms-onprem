
"""
   # -- -- do -- --
   if msg["type"] != "pmessage":
      print(f"BadMsg: {msg}")
   # -- -- do -- --
   if msg["pattern"].decode("utf-8") != self.chnl_pattern:
      print(f"BadPattern: {self.chnl_pattern}")
      return
   # -- -- do -- --
   data: str = msg["data"].decode("utf-8")
   if data[0] != "(" or data[-1] != ")":
      print("BadDataWrapper")
"""
import datetime


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class redSubMsg(object):

   MTYPE:  str = "pmessage"

   def __init__(self, d: {}):
      self.d = d
      self.mtype: str = d["type"]
      if self.mtype != redSubMsg.MTYPE:
         raise Exception(f"BadMsgType: {self.mtype}")
      self.patt: str = d["pattern"]
      self.data: str = d["data"]
      self.channel: str = d["channel"]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# qry = """select t.met_cir_rowid rowid
#       , t.cir_tag
#       , t.met_syspath spath
#       , t.elec_room_locl_tag ltag
#       , t.met_dt_crd
#    from core.elec_meter_circuits t;"""
class sysCircuit(object):

   def __init__(self, d: {}):
      self.met_cir_rowid: int = int(d[0])
      self.cir_tag: str = d[1]
      self.met_syspath: str = d[2]
      self.elc_room_tag: str = d[3]
      self.met_dt_crd: datetime.datetime = d[4]

   def __str__(self):
      return f"rowid: {self.met_cir_rowid} | cir_tag: {self.cir_tag} | spath: {self.met_syspath}"
