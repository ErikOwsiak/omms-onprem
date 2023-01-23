
import time, paramiko
from termcolor import colored
from paramiko.channel import Channel


KB_1 = 1024
MAX_LOOPS: int = 20
STEP_SLEEP_TINY: float = 1.0
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

   def run_cmd(self, cinfo: str, cmd: str, rpwd: str) -> []:
      root_prefix = "/r "
      if cmd.strip().startswith(root_prefix):
         lns: [] = self.__run_cmd_as_root(cinfo, rpwd, cmd.replace(root_prefix, ""))
      else:
         lns: [] = self.__run_cmd(cinfo, cmd)
      # -- -- -- --
      return lns

   def __run_cmd_as_root(self, cinfo, rpwd, cmd) -> []:
      # -- -- -- -- -- -- -- --
      err, shell = self.__get_root_channel(rpwd)
      if err != 0:
         pass
      # -- -- -- -- -- -- -- --
      shell: Channel = shell
      err, buff = self.__cmd_shell_resp(shell, cmd)
      return buff.splitlines()

   def __run_cmd(self, cinfo, cmd) -> []:
      shell: Channel = self.ssh_clt.invoke_shell()
      time.sleep(2.0)
      shell.in_buffer.empty()
      err, buff = self.__cmd_shell_resp(shell, cmd)
      return buff.splitlines()

   def __send_cmd_rec_resp(self, chnl: Channel
         , cmd: str
         , wait_tout: float
         , rec_len: int = 2048) -> str:
      try:
         if not cmd.endswith("\n"):
            cmd = f"{cmd}\n"
         chnl.in_buffer.empty()
         chnl.send(cmd.encode())
         time.sleep(wait_tout)
         rec_buff: bytes = chnl.recv(rec_len)
         if rec_buff in [None, []]:
            time.sleep(wait_tout * 2)
         return chnl.recv(rec_len).decode("utf-8")
      except Exception as e:
         print(e)
         return ""

   def __get_root_channel(self, su_pwd: str) -> (int, [None, Channel]):
      try:
         # -- -- -- --
         buff: str = ""; err_accu = 0
         shell: Channel = self.ssh_clt.invoke_shell()
         err, buff = self.__cmd_shell_resp(shell, "su", "password")
         err_accu += err
         if err != 0:
            pass
         err, buff = self.__cmd_shell_resp(shell, su_pwd, "root@")
         err_accu += err
         if err != 0:
            pass
         err, buff = self.__cmd_shell_resp(shell, "whoami", "root")
         err_accu += err
         if err != 0:
            pass
         # -- -- -- --
         return err_accu, shell
      except Exception as e:
         print(e)

   def __cmd_shell_resp(self, shell: Channel, cmd: str, patt: str = None) -> (bool, str):
      # -- -- -- -- -- -- -- --
      if not cmd.endswith("\n"):
         cmd = f"{cmd}\n"
      # -- -- -- -- -- -- -- --
      rec_buff: str = ""
      shell.in_buffer.empty()
      shell.send(cmd.encode())
      time.sleep(STEP_SLEEP_SHORT)
      lp_cnt: int = 0; pwd_prompt_found = False
      # -- -- -- -- -- -- -- --
      while lp_cnt < MAX_LOOPS:
         rec_buff += shell.recv(KB_1).decode("utf-8")
         time.sleep(STEP_SLEEP_TINY)
         if (patt is None) and (len(rec_buff)) > 0:
            break
         # -- -- --
         if patt not in rec_buff.lower():
            lp_cnt += 1
            continue
         else:
            pwd_prompt_found = True
            break
      # -- -- OUT OF MAIN LOOP -- --
      if (not pwd_prompt_found) and (lp_cnt == MAX_LOOPS):
         return 1, ""
      # -- -- -- --
      return 0, rec_buff.lower().strip()
