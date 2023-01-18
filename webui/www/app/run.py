#!/usr/bin/env python3

import cgi, os
import json
from re import U
from core.resp import resp
from core.pagebuff import pageBuffer
from core.guard import guard
from core.actions import actions
from core.sys import CTYPES, httpUtils, SYS_FILES_FOLDERS


try:
   HEADERS = []
   FORM = cgi.FieldStorage()
   ACTION = FORM.getvalue("action")
   ctype = ""; out = None
   # -- user login --
   if ACTION == "login":
      ctype = CTYPES.json
      omms_acl = actions.check_user(FORM)
      if omms_acl is False:  
         out = {"error": 100, "msg": "BadLogin"}
         HEADERS.append("Status: 307")
         HEADERS.append("Location: /login?msg=BadLogin")
      elif int(omms_acl) == 0:
         HEADERS.append("Status: 307")
         HEADERS.append("Location: /disabled")
      else:
         # out = {"error": 0, "msg": "GoodLogin", "acl": omms_acl}
         g: guard = guard()
         cookieHome, cookieLogout, cookieAcl, sessid = g.create_session(omms_acl)
         HEADERS.append(cookieHome)
         HEADERS.append(cookieLogout)
         HEADERS.append(cookieAcl)
         HEADERS.append(f"OpenBMSSessionID: {sessid}")
         uid: str = FORM.getvalue("UID")
         HEADERS.append(f"OMMS_USER: {uid}")
         HEADERS.append(f"OMMS_ACL: {omms_acl}")
         HEADERS.append("Status: 307")
         HEADERS.append(f"Location: /home?UID={uid}")
   # -- do logout --
   if ACTION == "logout":
      cookie = os.environ.get("HTTP_COOKIE", "")
      g: guard = guard(cookie)
      errnum, errstr, errmsg = g.check_session()
      if errnum == 0:
         g.end_session()
         jobj = {"error": 0, "msg": "removed", "nxturl": "/goodbye"}
         xresp: resp = resp(CTYPES.json, HEADERS)
         xresp.flush_string(json.dumps(jobj))
         xresp.the_end()
   # -- push back to client --
   xresp: resp = resp(CTYPES.html, HEADERS)
   xresp.flush_blank()
except Exception as e:
   pagebuff: pageBuffer = pageBuffer()
   pagebuff.load500(str(e))
   xresp: resp = resp(CTYPES.html, [])
   xresp.flush_page_buffer(pagebuff)
