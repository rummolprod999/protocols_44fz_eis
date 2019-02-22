import datetime
import logging
import traceback
from warnings import filterwarnings
import os
import pymysql

from ClassTypeProtocols504 import TypeProtocols504
from ClassTypeProtocols import TypeProtocols
from ClassProtocolEZP2 import parserEZP2
from ClassProtocolEZK2 import parserEZK2
from ClassProtocolEZP1 import parserEZP1
from ClassProtocolEOK1 import parserEOK1
from ClassProtocolEOK2 import parserEOK2
from ClassProtocolCancel import parserCancel
from ClassProtocolOK1 import parserOK1
from ClassProtocolOK2 import parserOK2
from ClassProtocolZK import parserZK
from ClassProtocolZPFinal import parserZPFinal
from ClassProtocolEF3 import parserEF3
from ClassProtocolEF1 import parserEF1
from ClassProtocolEF2 import parserEF2
from UtilsFunctions import logging_parser

if __name__ == "__main__":
    print('Привет, этот файл только для импортирования!')

EXECUTE_PATH = os.path.dirname(os.path.abspath(__file__))
PREFIX = ''
DB = 'tender'
LOG_D = 'log_prot'
LOG_DIR = f"{EXECUTE_PATH}/{LOG_D}"
TEMP_D = 'temp_prot'
TEMP_DIR = f"{EXECUTE_PATH}/{TEMP_D}"
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
filterwarnings('ignore', category=pymysql.Warning)
file_log = '{1}/protocol_ftp_{0}.log'.format(str(datetime.date.today()), LOG_DIR)
logging.basicConfig(level=logging.DEBUG, filename=file_log,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def parserEZP1Extract(doc, path_xml, filexml, reg, type_f):
    # TODO
    pass


def parserOther(doc, path_xml, filexml, reg, type_f):
    prot = doc[list(doc.keys())[0]]
    list_p = [v for v in prot.keys() if v.lower().startswith("ep")]
    if len(list_p) == 0:
        logging_parser("Can not find protocol tag", filexml)
        return
    if list_p[0] == TypeProtocols504.type_EZP1:
        parserEZP1(doc, path_xml, filexml, reg, TypeProtocols504.type_EZP1)
        pass
    elif list_p[0] == TypeProtocols504.type_EOK2:
        parserEOK2(doc, path_xml, filexml, reg, TypeProtocols504.type_EOK2)
        pass
    elif list_p[0] == TypeProtocols504.type_EOK1:
        parserEOK1(doc, path_xml, filexml, reg, TypeProtocols504.type_EOK1)
        pass
    elif list_p[0] == TypeProtocols504.type_EZK2:
        parserEZK2(doc, path_xml, filexml, reg, TypeProtocols504.type_EZK2)
        pass
    elif list_p[0] == TypeProtocols504.type_EZK1:
        parserEZK2(doc, path_xml, filexml, reg, TypeProtocols504.type_EZK1)
        pass
    elif list_p[0] == TypeProtocols504.type_EZP1Extract:
        parserEZP1Extract(doc, path_xml, filexml, reg, TypeProtocols504.type_EZP1Extract)
        pass
    if list_p[0] == TypeProtocols504.type_EZP2:
        parserEZP2(doc, path_xml, filexml, reg, TypeProtocols504.type_EZP2)
        pass
    else:
        logging_parser("New type protocol", list_p[0], path_xml)


def parser(doc, path_xml, filexml, reg, type_f):
    global file_log
    try:
        if type_f == TypeProtocols.type_EF1:
            parserEF1(doc, path_xml, filexml, reg, type_f)
            pass
        elif type_f == TypeProtocols.type_EF2:
            pass
            parserEF2(doc, path_xml, filexml, reg, type_f)
        elif (type_f == TypeProtocols.type_EF3 or type_f == TypeProtocols.type_EFSingleApp or
              type_f == TypeProtocols.type_EFSinglePart or type_f == TypeProtocols.type_Deviation or
              type_f == TypeProtocols.type_EFInvalidation):
            pass
            parserEF3(doc, path_xml, filexml, reg, type_f)
        elif type_f == TypeProtocols.type_ZK or type_f == TypeProtocols.type_ZKAfterProlong:
            pass
            parserZK(doc, path_xml, filexml, reg, type_f)
        elif (type_f == TypeProtocols.type_OK2 or type_f == TypeProtocols.type_OKD5 or
              type_f == TypeProtocols.type_OKOU3 or type_f == TypeProtocols.type_OKSingleApp or
              type_f == TypeProtocols.type_OKDSingleApp or type_f == TypeProtocols.type_OKOUSingleApp):
            pass
            parserOK2(doc, path_xml, filexml, reg, type_f)
        elif type_f == TypeProtocols.type_ZPFinal:
            pass
            parserZPFinal(doc, path_xml, filexml, reg, type_f)
        elif type_f == TypeProtocols.type_OK1 or type_f == TypeProtocols.type_OKD1 or type_f == TypeProtocols.type_OKD2 or \
                type_f == TypeProtocols.type_OKD3 or type_f == TypeProtocols.type_OKD4 or \
                type_f == TypeProtocols.type_OKOU1 or type_f == TypeProtocols.type_OKOU2:
            pass
            parserOK1(doc, path_xml, filexml, reg, type_f)
        elif type_f == TypeProtocols.type_Cancel:
            pass
            parserCancel(doc, path_xml, filexml, reg, type_f)
        else:
            parserOther(doc, path_xml, filexml, reg, type_f)
    except Exception as e:
        logging_parser("Ошибка в функции parser", e, path_xml, type_f)
        traceback.print_tb(e.__traceback__)
        pass
