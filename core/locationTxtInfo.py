
class locationTxtInfo:

   def __init__(self, path: str):
      self.path = path
      self.data: {} = {}

   def location(self):
      return self.__val__("location")

   def lat(self) -> float:
      return float(self.__val__("lat"))

   def lng(self):
      return float(self.__val__("lng"))

   def tz(self) -> str:
      return self.__val__("TZ")

   def region(self) -> str:
      return self.__val__("region")

   def load(self):
      with open(self.path, "r") as f:
         lns = f.readlines()
      for ln in lns:
         if ln.startswith("#"):
            continue
         arr = ln.strip().split(":=")
         if len(arr) != 2:
            continue
         key, val = arr
         self.data[key] = val
      return True

   def __val__(self, key):
      if key in self.data:
         return self.data[key]
      else:
         return None


"""
   DEFAULT_LOC_INFO locaiton loaded from working folder
"""
DEFAULT_LOC_INFO: locationTxtInfo = locationTxtInfo("location.txt")
DEFAULT_LOC_INFO.load()
