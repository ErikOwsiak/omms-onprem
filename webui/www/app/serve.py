#!/usr/bin/env python3

import os, cgi
from core.resp import resp
from core.pagebuff import pageBuffer
from core.guard import guard
from core.sys import CTYPES


login = "login"
allpages = ("home", "login", "goodbye", "err404", "err500")
cookiepages = ("home")
HEADERS = []


try:
   # -- create response buffer --
   pagebuff: pageBuffer = pageBuffer()
   # -- get request form --
   form = cgi.FieldStorage()
   page = form.getvalue("page")
   # -- test all endpoints --
   if not page in allpages:
      pagebuff.load404(page)
      xresp: resp = resp(CTYPES.html, [])
      xresp.flush_page_buffer(pagebuff)
      xresp.the_end(0)
   # -- test nocookie endpoints  --
   if not page in cookiepages:
      pagebuff.load(page)
      xresp: resp = resp(CTYPES.html, [])
      xresp.flush_page_buffer(pagebuff)
      xresp.the_end(0)
   # -- process cookie page --
   cookie = os.environ.get("HTTP_COOKIE", "")
   g: guard = guard(cookie)
   errnum, errstr, errmsg  = g.check_session()
   if errnum == 0:
      pagebuff.load(page)
   elif errnum in (100, 120):
      HEADERS.append("Status: 302")
      HEADERS.append(f"Location: /login?errstr={errstr}&c={errmsg}")
      xresp: resp = resp(CTYPES.html, HEADERS)
      xresp.flush_blank()
      xresp.the_end()
   # -- flush page --
   xresp: resp = resp(CTYPES.html, [])
   xresp.flush_page_buffer(pagebuff)
except Exception as e:
   pagebuff: pageBuffer = pageBuffer()
   pagebuff.load500(str(e))
   xresp: resp = resp(CTYPES.html, [])
   xresp.flush_page_buffer(pagebuff)
