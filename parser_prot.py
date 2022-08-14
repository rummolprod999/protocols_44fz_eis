import logging
import traceback
from warnings import filterwarnings
import os
import pymysql

import ClassProtocolCancel504
import ClassProtocolEOKOU1
import ClassProtocolEOKOU2
import ClassProtocolEOKOU3
import ClassProtocolEOKOUSingleApp
import ClassProtocolEOKOUSinglePart
import UtilsFunctions
from ClassPprf615ProtocolEF1 import parserPprf615ProtocolEF1
from ClassProtocolDeviation import parserProtocolDeviation
from ClassProtocolEF2020SubmitOffers import parserEF2020SubmitOffers
from ClassProtocolEOK2020Final import parserEOK2020Final
from ClassProtocolEOK2020SecondSections import parserEOK2020SecondSections
from ClassProtocolEZK2020FinalPart import parserEZK2020FinalPart
from ClassProtocolEZP1Extract import parserEZP1Extract
from ClassProtocolEZT2020Final import parserEZT2020Final
from ClassTypeProtocols504 import TypeProtocols504
from ClassTypeProtocols import TypeProtocols
from ClassProtocolEZP2 import parserEZP2
from ClassProtocolEZK2 import parserEZK2
from ClassProtocolEZP1 import parserEZP1
from ClassProtocolEOK1 import parserEOK1
from ClassProtocolEOK2 import parserEOK2
from ClassProtocolEOK3 import parserEOK3
from ClassProtocolCancel import parserCancel
from ClassProtocolOK1 import parserOK1
from ClassProtocolOK2 import parserOK2
from ClassProtocolZK import parserZK
from ClassProtocolZPFinal import parserZPFinal
from ClassProtocolEF3 import parserEF3
from ClassProtocolEF1 import parserEF1
from ClassProtocolEF2 import parserEF2
from ClassProtocolEFSinglePart import parserEFSinglePart
from ClassProtocolEOKOUSinglePart import parserEOKOUSinglePart
from ClassProtocolEOKOUSingleApp import parserEOKOUSingleApp
from ClassProtocolEF2020Final import parserEF2020Final
from UtilsFunctions import logging_parser
from VarExecut import LOG_DIR, file_log

if __name__ == "__main__":
    print('Привет, этот файл только для импортирования!')

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
filterwarnings('ignore', category=pymysql.Warning)
logging.basicConfig(level=logging.DEBUG, filename=file_log,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def parserOther(doc, path_xml, filexml, reg, type_f):
    prot = doc[list(doc.keys())[0]]
    list_p = [v for v in prot.keys() if (v.lower().startswith("ep") or v.lower().startswith("pprf"))]
    ex_type = ['PP615', 'Evasion', 'fcsProtocolPO', 'P615']
    for t in ex_type:
        if t in filexml:
            return
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
    elif list_p[0] == TypeProtocols504.type_EOKD1:
        parserEOK1(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKD1)
        pass
    elif list_p[0] == TypeProtocols504.type_EZK2:
        parserEZK2(doc, path_xml, filexml, reg, TypeProtocols504.type_EZK2)
        pass
    elif list_p[0] == TypeProtocols504.type_EZK1:
        parserEZK2(doc, path_xml, filexml, reg, TypeProtocols504.type_EZK1)
        pass
    elif list_p[0] == TypeProtocols504.type_EZP2:
        parserEZP2(doc, path_xml, filexml, reg, TypeProtocols504.type_EZP2)
        pass
    elif list_p[0] == TypeProtocols504.type_EF2020Final:
        parserEF2020Final(doc, path_xml, filexml, reg, TypeProtocols504.type_EF2020Final)
        pass
    elif list_p[0] == TypeProtocols504.type_EZK2020FinalPart:
        parserEZK2020FinalPart(doc, path_xml, filexml, reg, TypeProtocols504.type_EZK2020FinalPart)
        pass
    elif list_p[0] == TypeProtocols504.type_EF2020SubmitOffers:
        parserEF2020SubmitOffers(doc, path_xml, filexml, reg, TypeProtocols504.type_EF2020SubmitOffers)
        pass
    elif list_p[0] == TypeProtocols504.type_EOK3:
        parserEOK3(doc, path_xml, filexml, reg, TypeProtocols504.type_EOK3)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKOU2:
        ClassProtocolEOKOU2.parserEOKOU2(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKOU2)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKOU1:
        ClassProtocolEOKOU1.parserEOKOU1(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKOU1)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKSingleApp:
        parserEOK2020SecondSections(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKSingleApp)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKSinglePart:
        ClassProtocolEOKOU1.parserEOKOU1(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKSinglePart)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKOUSingleApp:
        ClassProtocolEOKOUSingleApp.parserEOKOUSingleApp(doc, path_xml, filexml, reg,
                                                         TypeProtocols504.type_EOKOUSingleApp)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKOUSinglePart:
        ClassProtocolEOKOUSinglePart.parserEOKOUSinglePart(doc, path_xml, filexml, reg,
                                                           TypeProtocols504.type_EOKOUSinglePart)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKOU3:
        ClassProtocolEOKOU3.parserEOKOU3(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKOU3)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKD4:
        ClassProtocolEOKOU3.parserEOKOU3(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKD4)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKDSingleApp:
        ClassProtocolEOKOU1.parserEOKOU1(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKDSingleApp)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKD2:
        ClassProtocolEOKOU1.parserEOKOU1(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKD2)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKD3:
        ClassProtocolEOKOU3.parserEOKOU3(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKD3)
        pass
    elif list_p[0] == TypeProtocols504.type_EOKDSinglePart:
        ClassProtocolEOKOU1.parserEOKOU1(doc, path_xml, filexml, reg, TypeProtocols504.type_EOKDSinglePart)
        pass
    elif list_p[0] == TypeProtocols504.type_epProtocolEOK2020SecondSections:
        parserEOK2020SecondSections(doc, path_xml, filexml, reg, TypeProtocols504.type_epProtocolEOK2020SecondSections)
        pass
    elif list_p[0] == TypeProtocols504.type_epProtocolEOK2020Final:
        parserEOK2020Final(doc, path_xml, filexml, reg, TypeProtocols504.type_epProtocolEOK2020Final)
        pass
    elif list_p[0] == TypeProtocols504.type_epProtocolDeviation:
        parserProtocolDeviation(doc, path_xml, filexml, reg, TypeProtocols504.type_epProtocolDeviation)
        pass
    elif list_p[0] == TypeProtocols504.type_epProtocolEZP1Extract:
        parserEZP1Extract(doc, path_xml, filexml, reg, TypeProtocols504.type_epProtocolEZP1Extract)
        pass
    elif list_p[0] == TypeProtocols504.type_pprf615ProtocolEF1:
        parserPprf615ProtocolEF1(doc, path_xml, filexml, reg, TypeProtocols504.type_pprf615ProtocolEF1)
        pass
    elif list_p[0] == TypeProtocols504.type_epProtocolEZT2020Final:
        parserEZT2020Final(doc, path_xml, filexml, reg, TypeProtocols504.type_epProtocolEZT2020Final)
        pass
    elif list_p[0] == TypeProtocols504.type_Cancel504:
        ClassProtocolCancel504.parserCancel504(doc, path_xml, filexml, reg, TypeProtocols504.type_Cancel504)
        pass
    else:
        logging_parser("New type protocol", list_p[0], path_xml)
        try:
            dir_xml = path_xml.replace(f"/{filexml}", "")
            # UtilsFunctions.copy_new_file(filexml, dir_xml)
        except Exception as ex1:
            logging.exception("Ошибка копирования файла: ")
            with open(file_log, 'a') as flog9:
                flog9.write('Ошибка копирования файла {0} {1}\n\n\n'.format(str(ex1), filexml))


def parser(doc, path_xml, filexml, reg, type_f):
    try:
        if type_f == TypeProtocols.type_EF1:
            parserEF1(doc, path_xml, filexml, reg, type_f)
            pass
        elif type_f == TypeProtocols.type_EF2:
            pass
            parserEF2(doc, path_xml, filexml, reg, type_f)
        elif (type_f == TypeProtocols.type_EF3 or type_f == TypeProtocols.type_EFSingleApp
              or type_f == TypeProtocols.type_Deviation or
              type_f == TypeProtocols.type_EFInvalidation or
              type_f == TypeProtocols.type_ProtocolEvasion):
            pass
            parserEF3(doc, path_xml, filexml, reg, type_f)
        elif type_f == TypeProtocols.type_EFSinglePart:
            pass
            parserEFSinglePart(doc, path_xml, filexml, reg, type_f)
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
            try:
                parserCancel(doc, path_xml, filexml, reg, type_f)
            except Exception:
                ClassProtocolCancel504.parserCancel504(doc, path_xml, filexml, reg, TypeProtocols504.type_Cancel504)
        else:
            parserOther(doc, path_xml, filexml, reg, type_f)
    except Exception as e:
        logging_parser("Ошибка в функции parser", e, traceback.format_exc(), path_xml, type_f)
        traceback.print_tb(e.__traceback__)
        pass
