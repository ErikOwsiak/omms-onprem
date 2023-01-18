
import hashlib
from typing import Tuple
from core.sys import SYS_FILES_FOLDERS


class actions(object):

   def __init__(self):
      pass

   """
      erik.owsiak;de8fb09e7f552feb243cc8386205e326;15;
   """
   @staticmethod
   def check_user(form) -> Tuple[bool, str]:
      # -- get data --
      uid: str = form.getvalue("UID")
      pwd: str = form.getvalue("PWD")
      # -- do md4 hash --
      md5 = hashlib.md5(pwd.encode("utf-8"))
      md5hash = md5.hexdigest()
      lines = None
      with open(SYS_FILES_FOLDERS.users, "r") as f:
         lines = f.readlines()
      arr = [ln for ln in lines if ln.startswith(f"{uid};")] 
      if len(arr) == 0:
         return False
      ln = arr[0]
      arr = ln.split(";")
      passok = (arr[1] == md5hash)
      if passok:
         return arr[2]
      else:
         return False

   @staticmethod
   def check_sess_token(token):
      return True
