
import time
from invoke import Responder
from invoke import Promise
from fabric import Connection, Config, Result


class edgeProxy(object):

   def __init__(self):
      pass

   def write_file(self, path: str, body: str):
      pass

   def do_cmd(self, uid: str, upwd: str, host: str, port: int, supwd: str, cmd: str):
      # -- -- -- -- --
      try:
         kwargs = {"password": upwd}
         host_buff = f"{uid}@{host}:{port}"
         conf: Config = Config(overrides={"root": {"password": supwd}})
         ssh_conn: Connection = Connection(host=host_buff, connect_kwargs=kwargs, config=conf)
         ssh_conn.open()
         if not ssh_conn.is_connected:
            print("not_connected")
            exit(1)
         # -- -- -- --
         su_pass: Responder = Responder(pattern=r"Password: ", response=f"{supwd}\n")
         prom: Promise = ssh_conn.run("su", pty=True, asynchronous=True, watchers=[su_pass])
         while True:
            time.sleep(0.200)
            if "assword:" in str(prom.runner.stdout):
               # print("got password")
               pass
            if "root@" in str(prom.runner.stdout):
               print("\n\t[ running as root ]\n")
               break
         # -- -- -- --
         res: Result = ssh_conn.run(cmd)
         for ln in res.stdout.splitlines():
            print(f"\t{ln}")
         print("\n\t[ RUN CMD END ]\n\n")
      except ConnectionError as e:
         print(e)
      except Exception as e:
         print(e)


# -- -- -- -- test ep -- -- -- --
if __name__ == "__main__":
   pass
