
import time


APPROOT = "/var/www/html"
SESSIONS_PATH = "/var/www/html/app/sessions"



class SYS_FILES_FOLDERS:

   cookieFolder = f"{APPROOT}/app/cookies"
   users = f"{APPROOT}/app/users"
   pagesFolder = f"{APPROOT}/pages"



class CTYPES:

   json = "application/json"
   html = "text/html"
   plain = "text/plain"



class httpUtils:

   @staticmethod
   def cookie_expires():
      end = time.gmtime(time.time() + (2 * 24 * 60 * 60))
      return time.strftime("%a, %d-%b-%Y %T GMT", end)
