import json


class gpioOpResp(object):

   def __init__(self, err: int, msg: str, bdy: str):
      self.err: int = err
      self.msg: str = msg
      self.bdy: str = bdy

   def toJson(self):
      d: {} = {"ERR": self.err, "MSG": self.msg, "BDY": self.bdy}
      return json.dumps(d)
