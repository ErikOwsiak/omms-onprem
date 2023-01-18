
import re, os.path, uuid
from typing import List, Tuple
import core.sys as xsys


sessName = "omms-session"
rx = r"omms-session=([a-z0-9]{32})"
ok = [0, "GoodCookie", ""]
exp = [1, "Exception", ""]
badCookie = [100, "BadCookie", ""]
badExpires = [110, "BadExpires", ""]
cookieNotFound = [120, "CookieNotFound", ""]


class guard(object):

   def __init__(self, rawcookie: str = ""):
      self.rawcookie = rawcookie
      self.arr = self.rawcookie.split(";")

   def check_session(self) -> List:
      try:
         sessid = self.__cookie_val__(sessName)
         cookiefile = f"{xsys.SYS_FILES_FOLDERS.cookieFolder}/cookie_{sessid}"
         if not os.path.exists(cookiefile):
            cookieNotFound[2] = sessid
            return cookieNotFound
         buff: str = ""
         with open(cookiefile, "r") as cf:
            buff = cf.read().strip()
         # -- bad cookie --
         # -- check cookie timeout --
         return ok
      except Exception as e:
         exp[2] = str(e)
         return exp

   def create_session(self, omms_acl) -> Tuple[str, str, str, str]:
      sessid = uuid.uuid4().hex
      expires = xsys.httpUtils.cookie_expires()
      # -- create local cookie file --
      cookiefile = f"{xsys.SYS_FILES_FOLDERS.cookieFolder}/cookie_{sessid}"
      with open(cookiefile, "w") as cf:
         cf.write(expires)
      # -- send cookie to the user -- 
      # domain = "85.222.109.238"
      host: str = os.environ.get("HTTP_HOST", "")
      domain = str(host.split(":")[0]).strip()
      # -- create cookies --
      cookie0 = f"Set-Cookie: {sessName}={sessid}; Expiers={expires};"\
            f" Domain={domain}; SameSite=Lax; Path=/home"
      cookie1 = f"Set-Cookie: {sessName}={sessid}; Expiers={expires};"\
            f" Domain={domain}; SameSite=Lax; Path=/do/logout"
      cookie2 = f"Set-Cookie: omms_acl={omms_acl}; Expiers={expires};"\
            f" Domain={domain}; SameSite=Lax; Path=/home"
      # -- return cookies --
      return cookie0, cookie1, cookie2, sessid

   def end_session(self):
      try:
         # -- 
         sessid = self.__cookie_val__(sessName)
         cookiefile = f"{xsys.SYS_FILES_FOLDERS.cookieFolder}/cookie_{sessid}"
         if not os.path.exists(cookiefile):
            cookieNotFound[2] = sessid
            return cookieNotFound
         # -- kill session --
         os.remove(cookiefile)
         return ok
      except Exception as e:
         exp[2] = str(e)
         return exp

   def __cookie_val__(self, name):
      for c in self.arr:
         if c.startswith(f"{name}="):
            return c.split("=")[1].strip(";")
      # -- end --
      return None
