#!/usr/bin/env python3

import cgi, cgitb
import requests


contentTypeJson = "Content-Type: application/json"
contentTypeError = "Content-Type: application/error"
contentTypeText = "Content-Type: text/plain"

logpath = "/var/log/iotech"
cgitb.enable(logdir=logpath)
host = "http://localhost:8082"
form = cgi.FieldStorage()
METHOD = ""
api = ""
tmp = None


try:
   if ("method" not in form) or ("api" not in form):
      print(contentTypeText)
      print()
      print("missing: method or api")
      print()
      exit(0)
   # -- run --
   METHOD = str(form.getvalue("method")).upper()
   api = form.getvalue("api")
except Exception as e:
   with open(f"{logpath}/last.exception", "w") as f:
      f.write(str(e))
   # -- dump page --
   print(contentTypeError)
   print(f"XCalledMethod: ?")
   print(f"XCalledAPI: ?")
   print()
   print(str(e))
   print()
   exit(0)


buff = ""
if api == "meters":
   flags: int = 0
   if "flags" in form:
      flags = int(form.getvalue("flags"))
   res = requests.get(f"{host}/{api}?flags={flags}")
   buff = res.text
elif api == "lastreading":
   tbl = form.getvalue("tbl")
   mid = form.getvalue("mid")
   callurl = f"{host}/streamer?streamTbl={tbl}&meterDBID={mid}"
   res = requests.get(callurl)
   buff = res.text
elif api == "org":
   res = requests.get(f"{host}/org")
   buff = res.text
elif api == "table-info":
   tbl = form.getvalue("tbl")
   res = requests.get(f"{host}/table-info?tbl={tbl}")
   buff = res.text
elif api == "elc-room-meters":
   etag = form.getvalue("entityTag")
   res = requests.get(f"{host}/elc-room-meters?entag={etag}")
   buff = res.text
elif api == "elc-room-meters-active":
   etag = form.getvalue("entityTag")
   res = requests.get(f"{host}/elc-room-meters-active?entag={etag}")
   buff = res.text
elif api == "clients":
   res = requests.get(f"{host}/clients")
   buff = res.text
elif api == "circuits":
   res = requests.get(f"{host}/circuits")
   buff = res.text
elif api == "histogram":
   mid = form.getvalue("mid")
   res = requests.get(f"{host}/histogram?mid={mid}")
   buff = res.text
elif api == "clt-circuits":
   res = requests.get(f"{host}/clt-circuits")
   buff = res.text
elif api == "config":
   # -- config --
   load = form.getvalue("load")
   if METHOD == "PUT":
      res = requests.put(f"{host}/config?load={load}")
      buff = res.text
   elif METHOD == "DEL":
      res = requests.delete(f"{host}/config?load={load}")
      buff = res.text
   else:
      pass
   # -- end config --
elif api == "report":
   rpt = form.getvalue("rpt")
   clttag = form.getvalue("clttag")
   sDate = form.getvalue("sd")
   eDate = form.getvalue("ed") 
   res = requests.get(f"{host}/report?repName={rpt}&cltTag={clttag}&sDate={sDate}&eDate={eDate}")
   buff = res.text
elif api == "datalists":
   dl = form.getvalue("dl")
   res = requests.get(f"{host}/datalists?dl={dl}")
   buff = res.text
elif api == "fetchcol":
   tbl = form.getvalue("tbl")
   col = form.getvalue("col")
   res = requests.get(f"{host}/fetchcol?tbl={tbl}&col={col}")
   buff = res.text
elif api == "table":
   args = ""
   tbl = form.getvalue("tbl")
   if "args" not in form:
      url = f"{host}/table?tbl={tbl}"
   else:
      args = form.getvalue("args")
      url = f"{host}/table?tbl={tbl}&args={args}"
   # -- call --
   res = requests.get(url)
   buff = res.text
else:
   buff = "BadShit!"

# -- dump page --
print(contentTypeJson)
print(f"XCalledMethod: {METHOD}")
print(f"XCalledAPI: {api}")
print()
print(buff)
print()
exit(0)
