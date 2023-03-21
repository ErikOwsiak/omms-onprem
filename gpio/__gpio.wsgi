import sys

APP_PATH = "/var/www/html/__m24__/qr_codes"
sys.path.insert(0, APP_PATH)
from qrcodes_app import app as application
