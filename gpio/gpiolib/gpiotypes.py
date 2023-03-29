
import json, os, sys
ROOT_DIR = os.getcwd()
try:
   from core.debug import debug
   from core.utils import sysUtils
   from ommslib.shared.core.datatypes import redisDBIdx
except Exception as e:
   print(e)
   print(ROOT_DIR)
   os.chdir("../")
   sys.path.append(os.getcwd())
   print(os.getcwd())
   from core.debug import debug
   from core.utils import sysUtils
   from ommslib.shared.core.datatypes import redisDBIdx
   os.chdir(ROOT_DIR)


class gpioOpResp(object):

   def __init__(self, err: int, msg: str, bdy: str):
      self.err: int = err
      self.msg: str = msg
      self.bdy: str = bdy

   def toJson(self):
      d: {} = {"ERR": self.err, "MSG": self.msg, "BDY": self.bdy}
      return json.dumps(d)


class confSetData(object):

   def __init__(self):
      self.jsobj: object = None
      self.devid: str = ""
      self.chnl: int = 0
      self.chnl_name: str = ""
      self.ON: str = ""
      self.OFF: str = ""
      self.dtsutc = sysUtils.dts_utc(with_tz=True)

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
         , "CONF_DTS": self.dtsutc, "OVERRIDE": "NIL", "OVERRIDE_DTS": "NIL"}


class forceData(object):

   def __init__(self):
      self.devid: str = ""
      self.chnl_id: int = 0
      self.state: str = ""
      self.dtsutc: str = sysUtils.dts_utc(with_tz=True)

   def load(self, jsobj: json):
      _on: [] = ["on", "ON", "1"]
      _off: [] = ["off", "OFF", "0"]
      self.devid = jsobj["devid"]
      self.chnl_id = int(jsobj["chnl"])
      self.state = jsobj["state"]

   def mapping(self) -> {}:
      return {"OVERRIDE": self.state, "OVERRIDE_DTS": self.dtsutc}
