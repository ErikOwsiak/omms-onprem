
import redis


class sessOps(object):

   def __init__(self, red: redis.Redis):
      self.red: redis.Redis = red

   def check(self):
      pass
