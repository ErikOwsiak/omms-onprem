
import time, paramiko
from termcolor import colored
from paramiko.channel import Channel

STEP_SLEEP_SHORT: float = 2.0
STEP_SLEEP_LONG: float = 4.0


class paramikoOps(object):

   def __init__(self):
      self.ssh_clt: paramiko.SSHClient = paramiko.SSHClient()

   def ssh_clt_connect(self, host: str, port: int, uid: str, pwd: str) -> bool:
      try:
         self.ssh_clt.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         self.ssh_clt.connect(hostname=host, port=port, username=uid, password=pwd)
         return self.ssh_clt.get_transport().is_active()
      except paramiko.ssh_exception.NoValidConnectionsError as e:
         print(colored(f"\n\t{str(e)}", "dark_grey"))
         return False
      except Exception as e:
         print(colored(f"\n\t{str(e)}", "dark_grey"))
         return False

   def run_as_root(self, conn, rpwd, cmd):
      shell: Channel = self.ssh_clt.invoke_shell()
      # Send the su command
      shell.in_buffer.empty()
      shell.send("su\n".encode())
      time.sleep(STEP_SLEEP_SHORT)
      # receive_buffer = shell.recv(1024)
      shell.in_buffer.empty()
      shell.send(rpwd + '\n')
      time.sleep(STEP_SLEEP_SHORT)
      # receive_buffer = shell.recv(1024)
      shell.in_buffer.empty()
      shell.send(f"{cmd}\n".encode())
      max_ticks = 20
      # -- -- -- -- -- -- -- -- -- -- -- --
      while not shell.recv_ready():
         time.sleep(0.2)
         max_ticks -= 1
         if max_ticks == 0:
            print("MAX_TICKS_IS_ZERO")
            raise Exception("MAX_TICKS_IS_ZERO")
      time.sleep(STEP_SLEEP_LONG)
      lns = shell.recv(4096).splitlines()
      # -- -- -- -- display -- -- -- --
      print(colored(f"\n\t[ CONN:: {conn} ]", "blue"))
      print(colored(f"\t[ CMD:: {lns[0].decode()} ]", "green"))
      for ln in lns[1:-1]:
         print(colored(f"\t    > {ln.decode()}", "light_blue"))
      shell.in_buffer.empty()
      print(colored("\t--- end ---\n", "red"))
      # -- -- -- -- end -- -- -- --
