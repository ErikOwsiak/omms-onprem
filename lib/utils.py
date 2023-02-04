

from textwrap import wrap
from termcolor import colored


class utils(object):

   @staticmethod
   def arr_dict(arr: [], dlm: str) -> {}:
      _out: {} = {}
      for a in arr:
         p = a.find(dlm)
         k, v = a[0:p], a[(p + 1):]
         _out[str(k)] = v
      # -- -- -- --
      return _out

   @staticmethod
   def txt_block_formatted(msg: str, **kwargs) -> []:
      """
         black, red, green, yellow, blue, magenta, cyan, white,
         light_grey, dark_grey, light_red, light_green, light_yellow, light_blue,
         light_magenta, light_cyan
      """
      tabs = 2
      if "tabs" in kwargs.keys():
         pass
      chars = 76
      if "chars" in kwargs.keys():
         pass
      color = "green"
      if "color" in kwargs.keys():
         pass
      lns = wrap(msg, chars)
      return [colored(f"\t{ln}", color) for ln in lns]
