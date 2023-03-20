#!/usr/bin/env python3

import json, os.path
import configparser as _cp, redis, setproctitle
from flask import Flask, render_template, request as req, make_response
from core.debug import debug
# from psql.dbConnServer import dbConnServer
# from core.logProxy import logProxy


# -- load ini file --
GPIO_INI_FILE = "gpio.ini"
if not os.path.exists(GPIO_INI_FILE):
   print(f"PathNotFound: {GPIO_INI_FILE}")
   exit(-1)
GPIO_INI: _cp.ConfigParser = _cp.ConfigParser()
GPIO_INI.read(GPIO_INI_FILE)
HTTP_PORT: int = GPIO_INI.getint("HTTP", "PORT")

# -- -- -- --
REDIS_SEC = "REDIS_PROD"
if debug.is_dev_box():
   REDIS_SEC = "REDIS_DEV"

# -- -- -- --
RED: _cp.SectionProxy = GPIO_INI[REDIS_SEC]
RED_CORE: _cp.SectionProxy = GPIO_INI["REDIS_CORE"]
REDIS: redis.Redis = redis.Redis(host=RED.get("HOST")
   , port=RED.getint("PORT"), password=RED_CORE.get("PWD"))
if not REDIS.ping():
   print("RedisBadPing!")
   exit(2)


CTYPE_JSON = "text/json"
CTYPE_TEXT = "text/plain"


APP_NAME = "gpio-webui"
app = Flask(APP_NAME, static_url_path=""
   , static_folder="www", template_folder="www")


@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def index():
   mode = ""; key = "mode"
   if key in req.args:
      mode = req.args[key]
   # -- --
   if mode == "iframe":
      buff = render_template("iframe.html", _mode=mode)
   else:
      buff = render_template("idx.html")
   # -- --
   return buff


"""
   "/api/get/list-reports";
"""
@app.route("/info")
def state_info():
   hdrs = {"AppServer": "dbEdit ver.: 0.0.3", "content-type": "text/json"}
   try:
      d: {} = {"INFO": "GPIO-WEBUI"}
      # -- return --
      return json.dumps(d), 200, hdrs
   except Exception as e:
      print(e)


# == == == == == == == == == == == == == == == == == == == == == ==
# -- -- [ start app here ] -- --
if __name__ == "__main__":
   print(os.getcwd())
   setproctitle.setproctitle(APP_NAME)
   app.run(host="0.0.0.0", port=HTTP_PORT)
# == == == == == == == == == == == == == == == == == == == == == ==
