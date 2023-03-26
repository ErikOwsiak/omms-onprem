
import os, sys, redis
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
   os.chdir("gpio")


class gpioOps(object):

   def __init__(self, red: redis.Redis):
      self.red: redis.Redis = red

   def override(self):
      pass

   def setconf(self):
      pass

   def getconf(self):
      pass
