

class gpioOpResp(object):

   def __init__(self, err: int, msg: str, bdy: str):
      self.err: int = err
      self.msg: str = msg
      self.bdy: str = bdy
