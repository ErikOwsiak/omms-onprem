
import time
from termcolor import colored
from core.edgeProxy import edgeProxy
from core.paramikoOps import paramikoOps


class edgeOps(object):

   def __init__(self):
      self.epxy: edgeProxy = None
      self.edgeops: paramikoOps = paramikoOps()

   def run_edge_cmd(self, edges: []):
      cb = colored("exp: ps -A | grep omms- ", "yellow")
      txt = f"\n\t\tenter cmd {cb}: "
      cmd = input(txt)
      for e in edges:
         self.__cmd_on_edge(cmd, e)

   def __cmd_on_edge(self, cmd, edge: str):
      # -- -- -- -- -- -- -- --
      hinfo, usr, su = edge.split(";")
      self.epxy: edgeProxy = edgeProxy()
      host, ip, port = [v.strip() for v in hinfo.split(" ")]
      u_uid, u_pwd = [v.strip() for v in usr.strip().split(" ")]
      su_uid, su_pwd = [v.strip() for v in su.strip().split(" ")]
      # -- -- -- -- -- -- -- --
      if not self.edgeops.ssh_clt_connect(ip, port, u_uid, u_pwd):
         print(colored("\tSHHClientNotConnected", "red"))
         return
      self.edgeops.run_as_root(f"{host}/{ip}:{port}", su_pwd, cmd)
