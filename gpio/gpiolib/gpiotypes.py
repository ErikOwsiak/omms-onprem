
import json, os, sys
try:
   from core.debug import debug
   from core.utils import sysUtils
   from ommslib.shared.core.datatypes import redisDBIdx
except Exception as e:
   print(os.getcwd())
   os.chdir("../")
   sys.path.append(os.getcwd())
   print(os.getcwd())
   from core.debug import debug
   from core.utils import sysUtils
   from ommslib.shared.core.datatypes import redisDBIdx


class gpioOpResp(object):

   def __init__(self, err: int, msg: str, bdy: str):
      self.err: int = err
      self.msg: str = msg
      self.bdy: str = bdy

   def toJson(self):
      d: {} = {"ERR": self.err, "MSG": self.msg, "BDY": self.bdy}
      return json.dumps(d)


"""
   let data = {"devid": t.devid, "chnl": t.chnl, chnlName
      , "ON": `${onHH}:${onMM}`, "OFF": `${offHH}:${offMM}`};
"""
class confSetData(object):

   def __init__(self):
      self.jsobj: object = None
      self.devid: str = ""
      self.chnl: int = 0
      self.chnl_name: str = ""
      self.ON: str = ""
      self.OFF: str = ""
      self.dtsutc = sysUtils.dts_utc()

   def load(self, jsobj: json):
      self.jsobj = jsobj
      self.devid: str = self.jsobj["devid"]
      self.chnl: int = int(self.jsobj["chnl"])
      self.chnl_name: str = self.jsobj["chnlName"]
      self.ON: str = self.jsobj["ON"]
      self.OFF: str = self.jsobj["OFF"]

   def mapping(self) -> {}:
      return {"DEVICE_ID": self.devid, "BOARD_CHANNEL": self.chnl
         , "CHANNEL_NAME": self.chnl_name, "ON": self.ON, "OFF": self.OFF
         , "OVERRIDE": "NIL", "DTSUTC": self.dtsutc}


class forceData(object):

   def __init__(self):
      self.devid: str = ""
      self.chnl_id: int = 0
      self.state: str = ""
      self.dtsutc: str = sysUtils.dts_utc()

   """
      _data: {} = {"CHANNEL_ID": chnl, "OVERRIDE": json.dumps(jsobj)}
   """
   def load(self, jsobj: json):
      _on: [] = ["on", "ON", "1"]
      _off: [] = ["off", "OFF", "0"]
      self.devid = jsobj["devid"]
      self.chnl_id = int(jsobj["chnl"])
      self.state = jsobj["state"]

   def mapping(self) -> {}:
      return {"OVERRIDE": self.state, "OVERRIDE_DTSUTC": self.dtsutc}
