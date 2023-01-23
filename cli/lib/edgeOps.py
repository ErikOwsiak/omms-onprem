
from termcolor import colored
from core.edgeProxy import edgeProxy
from core.paramikoOps import paramikoOps


class edgeOps(object):

   def __init__(self):
      self.epxy: edgeProxy = None
      self.edgeops: paramikoOps = paramikoOps()

   def run_edge_cmd(self, edges: []):
      cb = colored("exp: /r <- as root ps -A | grep omms- ", "yellow")
      txt = f"\n\t\tenter cmd {cb}: "
      cmd = input(txt)
      for e in edges:
         self.__cmd_on_edge(cmd, e)
      # -- user input --
      v = input("\n\tHit any key to continue:\n\n")

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
      try:
         conn_tag: str = f"{host} / {ip}:{port}"
         lns = self.edgeops.run_cmd(conn_tag, cmd, su_pwd)
         # -- -- print -- --
         ctxt = colored(f"\n\t[ {conn_tag} ]", "blue")
         print(ctxt)
         for ln in lns:
            print(f"\t  {ln}")
         self.edgeops.ssh_clt.close()
      except Exception as e:
         print(e)
