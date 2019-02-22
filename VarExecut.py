import datetime
import os

EXECUTE_PATH = os.path.dirname(os.path.abspath(__file__))
PREFIX = ''
DB = 'tender'
LOG_D = 'log_prot'
LOG_DIR = f"{EXECUTE_PATH}/{LOG_D}"
TEMP_D = 'temp_prot'
TEMP_DIR = f"{EXECUTE_PATH}/{TEMP_D}"
file_log = '{1}/protocol_ftp_{0}.log'.format(str(datetime.date.today()), LOG_DIR)
