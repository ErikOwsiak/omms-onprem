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
API = ""
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
   API = str(form.getvalue("api"))
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
if API == "histogram":
   # ^(get)/v1/(histogram)/([3|6|12|24])/(.*)$ api_v1.py?method=$1&api=$2$hrs=$3&mid=$4
   hrs = form.getvalue("hrs")
   mid = form.getvalue("mid")
   res = requests.get(f"{host}/histogram?mid={mid}&hrs={hrs}")
   buff = res.text
elif API == "edgestats":
   hostname = hrs = form.getvalue("hostname")
   res = requests.get(f"{host}/edgestats?hostname={hostname}")
   buff = res.text
elif API == "overview":
   res = requests.get(f"{host}/sys-overview")
   buff = res.text
   # -- end config --
else:
   buff = f"BadShit!:: {API}"

# -- dump page --
print(contentTypeJson)
print(f"XCalledMethod: {METHOD}")
print(f"XCalledAPI: {API}")
print()
print(buff)
print()
exit(0)
