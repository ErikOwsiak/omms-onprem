import sys

APP_PATH = "/opt/iotech/omms-onprem/webui"
sys.path.insert(0, APP_PATH)
from webapp import app as application
