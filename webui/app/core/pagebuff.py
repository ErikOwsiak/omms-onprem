#!/usr/bin/env python3

import os.path, re
from core.sys import SYS_FILES_FOLDERS


# <META HTTP-EQUIV="Refresh" CONTENT="0;URL=http://www.some.org/some.html">


class pageBuffer(object):

   def __init__(self):
      self.page = None
      self.buff = None
      self.httpCode = None
      self.redirectUrl = None

   def load(self, page):
      try:
         self.page = page
         pagefile = f"{SYS_FILES_FOLDERS.pagesFolder}/__{self.page}__.html"
         if not os.path.exists(pagefile):
            f404 = f"{SYS_FILES_FOLDERS.pagesFolder}/__err404__.html"
            self.buff = self.__load_pagefile__(f404)
            self.httpCode = 404
         else:
            self.httpCode = 200
            self.buff = self.__load_pagefile__(pagefile)
      except Exception as e:
         self.httpCode = 500
         self.buff = self.__load_err__(self.httpCode, str(e))

   def load404(self, msg: str):
      self.httpCode = 404
      self.buff = self.__load_err__(self.httpCode, msg)

   def load500(self, msg: str):
      self.httpCode = 500
      self.buff = self.__load_err__(self.httpCode, msg)

   def __process_includes__(self, ln) -> str:
      if not "<!--#include" in ln:
         return ln
      else:
         # <!--#include virtual="/xml/reports.xml" -->
         patt = r"virtual=\"/(?P<path>[a-zA-Z0-9\-\./]{4,32})\""
         m = re.search(patt, ln)
         if m:
            path = m.group("path")
            fullpath = f"../{path}"
            if os.path.exists(fullpath):
               with open(fullpath, "r") as f:
                  buff = f.read()
            else:
               buff = "<!-- bad file path :: check file for errors -->"
            return buff
         else:
            return "NoMatch"

   def __load_pagefile__(self, pagefile):
      out = []
      filelines = []
      with open(pagefile, "r") as f:
         filelines = f.readlines()
      for ln in filelines:
         newln = self.__process_includes__(ln)
         out.append(newln)
      return "".join(out)

   def __load_err__(self, errcode, errsmg):
      errfile = f"{SYS_FILES_FOLDERS.pagesFolder}/__err{errcode}__.html"
      with open(errfile, "r") as f:
         errbuff: str = f.read()
      return errbuff.replace("%ERRORBUFF%", str(errsmg))
