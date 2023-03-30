
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
