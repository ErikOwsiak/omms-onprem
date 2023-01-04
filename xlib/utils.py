

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
