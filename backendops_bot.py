#!/usr/bin/env python3

import time, psutil, os
import threading as th
import configparser as _cp
import setproctitle, redis
# -- system --
from core.debug import debug
from core.redis2psql import redis2psql
from core.utils import sysUtils as utils
from psql.dbConnServer import dbConnServer
from core.backendOps import backendOps


INI: _cp.ConfigParser = _cp.ConfigParser()
INI.read("conf/system.ini")


# -- -- -- -- -- -- -- --
PROC_NAME = "omms-backend"
RED_CONN_SEC_INI = INI["REDIS_PROD"]
PSQL_CONN_SEC_INI = INI["PSQL_PROD"]
if debug.is_dev_box():
   RED_CONN_SEC_INI = INI["REDIS_DEV"]
   PSQL_CONN_SEC_INI = INI["PSQL_DEV"]
# -- -- -- -- -- -- -- --
REDIS_PWD = INI["REDIS"]["PWD"]
REDIS_HOST = RED_CONN_SEC_INI["HOST"]
REDIS_PORT: int = int(RED_CONN_SEC_INI["PORT"])
PSQL_CONN_STR: str = PSQL_CONN_SEC_INI["CONN_STR"]


# -- check reports path --
path: str = INI.get("BACKEND", "REPORTS_PATH")
if not os.path.exists(path):
   print(f"PathNotFound: {path}")
   exit(1)


# -- dev box --
RED: redis.Redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PWD)
if not RED.ping():
   print(f"Can't Ping Redis Server: {REDIS_HOST}:{REDIS_PORT}")
   exit(2)

# -- redis to psql object --
PSQL_CONN = dbConnServer.getConnection(PSQL_CONN_STR)
BACKEND_OPS: backendOps = backendOps(INI, RED, psqlConnStr=PSQL_CONN_STR)
BACKEND_OPS.init()
BACKEND_OPS.run_main_thread()

def main():
   setproctitle.setproctitle(PROC_NAME)
   while True:
      time.sleep(8.0)
      print("backendops_bot_main")


# -- -- [ start here ] -- --
if __name__ == "__main__":
   main()
