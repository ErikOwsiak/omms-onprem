
import json, sys
from typing import List
from core.pagebuff import pageBuffer
from core.sys import CTYPES


class resp(object):

   def __init__(self, ctype: str, hdrs: List = []):
      self.buff: object = None
      self.ctype = ctype
      self.hdrs = hdrs

   def flush_page_buffer(self, pagebuff: pageBuffer):
      self.__flush_headers__()
      print(f"Content-Type: {self.ctype}")
      print()
      print(pagebuff.buff)
      print()

   def the_end(self, code: int = 0):
      sys.exit(code)

   def flush_blank(self):
      self.__flush_headers__()
      print(f"Content-Type: {self.ctype}")
      print()
      print("")
      print()

   def flush_string(self, buff):
      self.__flush_headers__()
      print(f"Content-Type: {self.ctype}")
      print()
      print(buff)
      print()

   def __setbuff__(self):
      if self.ctype == CTYPES.html:
         self.buff = self.buff
      if self.ctype == CTYPES.json:
         self.buff = json.dumps(self.buff)

   def __flush_headers__(self):
      _ = [h for h in self.hdrs if print(h) or True]
