import datetime
import ftplib
import logging
import os
import shutil
import sys
import time
import zipfile
import timeout_decorator
import xmltodict

import ClassProtocolCancel
import ClassProtocolCancel504
import ClassProtocolEF1
import ClassProtocolEF2
import ClassProtocolEF3
import ClassProtocolEOK1
import ClassProtocolEOK2
import ClassProtocolEOK3
import ClassProtocolEOKOU1
import ClassProtocolEOKOU2
import ClassProtocolEOKOU3
import ClassProtocolEZK2
import ClassProtocolEZP1
import ClassProtocolEZP2
import ClassProtocolEF2020Final
import ClassProtocolOK1
import ClassProtocolOK2
import ClassProtocolZK
import ClassProtocolZPFinal
import ClassTypeProtocols
import ClassProtocolEFSinglePart
import ClassTypeProtocols504
import ClassProtocolEOKOUSingleApp
import UtilsFunctions
import VarExecut
import parser_prot as parser_protocol
from ClassAddInfo import ProtocolAddInfo
from ClassPprf615ProtocolEF1 import Pprf615ProtocolEF1
from ClassPprf615ProtocolEF2 import Pprf615ProtocolEF2
from ClassPprf615ProtocolPO import Pprf615ProtocolPO
from ClassPprf615QualifiedContractor import Pprf615QualifiedContractor
from ClassProposalsResult import ProtocolProposalsResult
from ClassProtocolAddInfoInvalid import ProtocolAddInfoInvalid
from ClassProtocolDeviation import ProtocolDeviation
from ClassProtocolEF2020SubmitOffers import ProtocolEF2020SubmitOffers
from ClassProtocolEOK2020Final import ProtocolEOK2020Final
from ClassProtocolEOK2020SecondSections import ProtocolEOK2020SecondSections
from ClassProtocolEOKOU1New import ProtocolEOKOU1New
from ClassProtocolEZK2020FinalPart import ProtocolEZK2020FinalPart
from ClassProtocolEZP1Extract import ProtocolEZP1Extract
from ClassProtocolEZT2020Final import ProtocolEZT2020Final
from connect_to_db import connect_bd

PREFIX = VarExecut.PREFIX
DB = VarExecut.DB
TEMP_DIR = VarExecut.TEMP_DIR
LOG_DIR = VarExecut.LOG_DIR
file_log = VarExecut.file_log
logging.basicConfig(level=logging.DEBUG, filename=file_log,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
except_file = ()

logging_parser = UtilsFunctions.logging_parser


def get_xml_to_dict(filexml, dirxml, region, type_f):
    """
    :param filexml: имя xml
    :param dirxml: путь к локальному файлу
    :return:
    """
    try:
        # UtilsFunctions.unic(filexml, dirxml)
        pass
    except Exception as ex1:
        logging.exception("Ошибка копирования файла: ")
        with open(file_log, 'a') as flog9:
            flog9.write('Ошибка копирования файла {0} {1}\n\n\n'.format(str(ex1), filexml))
    path_xml = dirxml + '/' + filexml
    # print(path_xml)
    with open(path_xml) as fd:
        try:
            firs_str = fd.read()
            if True:
                firs_str = firs_str.replace("xmlns:ns1", "xmlnsns1").replace("xmlns:ns2", "xmlnsns2").replace(
                        "xmlns:ns3", "xmlnsns3").replace("xmlns:ns4", "xmlnsns4") \
                    .replace("xmlns:ns5", "xmlnsns5").replace("xmlns:ns6", "xmlnsns6").replace("xmlns:ns7",
                                                                                               "xmlnsns7").replace(
                        "xmlns:ns8", "xmlnsns8").replace(
                        "xmlns:ns9", "xmlnsns9")
                firs_str = firs_str.replace("ns1:", "").replace("ns2:", "").replace("ns3:", "").replace("ns4:", "") \
                    .replace("ns5:", "").replace("ns6:", "").replace("ns7:", "").replace("ns8:", "").replace("ns9:", "")
            doc = xmltodict.parse(firs_str)
            parser_protocol.parser(doc, path_xml, filexml, region, type_f)

            # with open(file_count_god, 'a') as good:
            #     good.write(str(count_good) + '\n')

        except Exception as ex:
            logging.exception("Ошибка: ")
            with open(file_log, 'a') as flog:
                flog.write("Ошибка конвертации в словарь " + str(ex) + ' ' + path_xml + '\n\n\n')

                # with open(file_count_bad, 'a') as bad:
                #     bad.write(str(count_bad) + '\n')
                # return


def bolter(file, l_dir, region, type_f):
    """
    :param file: файл для проверки на черный список
    :param l_dir: директория локального файла
    :return: Если файл есть в черном списке - выходим
    """
    file_lower = file.lower()
    if not file_lower.endswith('.xml'):
        return
    for g in except_file:
        if file_lower.find(g.lower()) != -1:
            return
    # print(f)
    try:
        get_xml_to_dict(file, l_dir, region, type_f)
    except Exception as exppars:
        # print('Не удалось пропарсить файл ' + str(exppars) + ' ' + file)
        logging.exception("Ошибка: ")
        with open(file_log, 'a') as flog:
            flog.write(f'Не удалось пропарсить файл {str(exppars)} {file}\n')


def get_list_ftp_curr(path_parse, region):
    """
    :param region: регион архива
    :param path_parse: путь для архивов региона
    :return: возвращаем список архивов за 2016, 2017, 2018, 2019, 2020
    """
    host = 'ftp.zakupki.gov.ru'
    ftpuser = 'free'
    password = 'VNIMANIE!_otkluchenie_FTP_s_01_01_2025_podrobnee_v_ATFF'
    with ftplib.FTP(host) as ftp2:
        ftp2.set_debuglevel(0)
        ftp2.encoding = 'utf8'
        ftp2.login(ftpuser, password)
        ftp2.cwd(path_parse)
        data = ftp2.nlst()
        array_ar = []
        con_arhiv = connect_bd(DB)
        cur_arhiv = con_arhiv.cursor()
        for i in data:
            if i.find('2016') != -1 or i.find('2017') != -1 or i.find('2018') != -1 or i.find('2019') != -1 or i.find(
                    '2020') != -1 or i.find('2021') != -1 or i.find('2022') != -1 or i.find('2023') != -1 or i.find(
                    '2024') != -1:
                i_new = path_parse + i
                cur_arhiv.execute(f"""SELECT id FROM {PREFIX}arhiv_prot WHERE arhiv = %s AND region = %s""",
                                  (i_new, region))
                find_file = cur_arhiv.fetchone()
                if find_file:
                    continue
                else:
                    array_ar.append(i)
                    query_ar = f"""INSERT INTO {PREFIX}arhiv_prot SET arhiv = %s, region = %s"""
                    query_par = (i_new, region)
                    cur_arhiv.execute(query_ar, query_par)
                    # with open(file_log, 'a') as flog5:
                    #     flog5.write('Добавлен новый архив ' + i + '\n')
        cur_arhiv.close()
        con_arhiv.close()
        return array_ar


def get_list_ftp_prev(path_parse, region):
    """
    :param region: регион архива
    :param path_parse: путь для архивов региона
    :return: возвращаем список архивов за 2016, 2017, 2018
    """
    host = 'ftp.zakupki.gov.ru'
    ftpuser = 'free'
    password = 'VNIMANIE!_otkluchenie_FTP_s_01_01_2025_podrobnee_v_ATFF'
    with ftplib.FTP(host) as ftp2:
        ftp2.set_debuglevel(0)
        ftp2.encoding = 'utf8'
        ftp2.login(ftpuser, password)
        ftp2.cwd(path_parse)
        data = ftp2.nlst()
        array_ar = []
        con_arhiv = connect_bd(DB)
        cur_arhiv = con_arhiv.cursor()
        # searchstring = datetime.datetime.now().strftime('%Y%m%d')
        for i in data:
            i_prev = path_parse + i
            if True:
                cur_arhiv.execute(f"""SELECT id FROM {PREFIX}arhiv_prot WHERE arhiv = %s AND region = %s""",
                                  (i_prev, region))
                find_file = cur_arhiv.fetchone()
                if find_file:
                    continue
                else:
                    array_ar.append(i)
                    query_ar = f"""INSERT INTO {PREFIX}arhiv_prot SET arhiv = %s, region = %s"""
                    query_par = (i_prev, region)
                    cur_arhiv.execute(query_ar, query_par)
                    # with open(file_log, 'a') as flog5:
                    #     flog5.write('Добавлен новый архив ' + i + '\n')
        cur_arhiv.close()
        con_arhiv.close()
        return array_ar


def get_list_ftp_last(path_parse):
    """
    :param path_parse: путь для архивов региона
    :return: возвращаем список архивов за 2016, 2017, 2018
    """
    host = 'ftp.zakupki.gov.ru'
    ftpuser = 'free'
    password = 'VNIMANIE!_otkluchenie_FTP_s_01_01_2025_podrobnee_v_ATFF'
    with ftplib.FTP(host) as ftp2:
        ftp2.set_debuglevel(0)
        ftp2.encoding = 'utf8'
        ftp2.login(ftpuser, password)
        ftp2.cwd(path_parse)
        data = ftp2.nlst()
        array_ar = []
        for i in data:
            if i.find('2022') != -1:
                array_ar.append(i)

        return array_ar


def extract_prot(m, path_parse1, region):
    """
    :param m: имя архива с контрактами
    :param path_parse1: путь до папки с архивом
    """
    global need_file
    l = get_ar(m, path_parse1)
    if l:
        # print(l)
        r_ind = l.rindex('.')
        l_dir = l[:r_ind]
        os.mkdir(l_dir)
        try:
            z = zipfile.ZipFile(l, 'r')
            z.extractall(l_dir)
            z.close()
        except UnicodeDecodeError as ea:
            # print('Не удалось извлечь архив ошибка UnicodeDecodeError ' + str(ea) + ' ' + l)
            with open(file_log, 'a') as floga:
                floga.write(f'Не удалось извлечь архив ошибка UnicodeDecodeError {str(ea)} {l}\n')
            try:
                os.system('unzip %s -d %s' % (l, l_dir))
                logging_parser("Извлекли архив альтернативным методом", l)
            except Exception as ear:
                # print('Не удалось извлечь архив альтернативным методом')
                with open(file_log, 'a') as flogb:
                    flogb.write(f'Не удалось извлечь архив альтернативным методом {str(ear)} {l}\n')
                return
        except Exception as e:
            # print('Не удалось извлечь архив ' + str(e) + ' ' + l)
            logging.exception("Ошибка: ")
            with open(file_log, 'a') as flogc:
                flogc.write(f'Не удалось извлечь архив {str(e)} {l}\n')
            return

        try:
            file_list = os.listdir(l_dir)
            list_type_EF1 = [file for file in file_list if (
                        file.find(ClassTypeProtocols.TypeProtocols.type_EF1) != -1 and file.find(
                    ClassTypeProtocols504.TypeProtocols504.type_pprf615ProtocolEF1) == -1)]
            list_type_EF2 = [file for file in file_list if
                             (file.find(ClassTypeProtocols.TypeProtocols.type_EF2) != -1 and file.find(
                                     ClassTypeProtocols504.TypeProtocols504.type_EF2020Final) == -1 and file.find(
                                     ClassTypeProtocols504.TypeProtocols504.type_EF2020SubmitOffers) == -1 and file.find(
                                     ClassTypeProtocols504.TypeProtocols504.type_pprf615ProtocolEF2) == -1)]
            list_type_EF3 = [file for file in file_list if file.find(ClassTypeProtocols.TypeProtocols.type_EF3) != -1]
            list_type_ZK = [file for file in file_list if file.find(ClassTypeProtocols.TypeProtocols.type_ZK) != -1]
            list_type_ZKAfterProlong = [file for file in file_list if
                                        file.find(ClassTypeProtocols.TypeProtocols.type_ZKAfterProlong) != -1]
            list_type_EFSingleApp = [file for file in file_list if
                                     file.find(ClassTypeProtocols.TypeProtocols.type_EFSingleApp) != -1]
            list_type_EFSinglePart = [file for file in file_list if
                                      file.find(ClassTypeProtocols.TypeProtocols.type_EFSinglePart) != -1]
            list_type_OK2 = [file for file in file_list if file.find(ClassTypeProtocols.TypeProtocols.type_OK2) != -1]
            list_type_OKD5 = [file for file in file_list if file.find(ClassTypeProtocols.TypeProtocols.type_OKD5) != -1]
            list_type_OKOU3 = [file for file in file_list if file.find(
                    ClassTypeProtocols.TypeProtocols.type_OKOU3) != -1]
            list_type_ZPFinal = [file for file in file_list if
                                 file.find(ClassTypeProtocols.TypeProtocols.type_ZPFinal) != -1]
            list_type_Deviation = [file for file in file_list if
                                   file.find(ClassTypeProtocols.TypeProtocols.type_Deviation) != -1 and file.find(
                                           ClassTypeProtocols504.TypeProtocols504.type_epProtocolDeviation) == -1
                                   and file.find(
                                           ClassTypeProtocols504.TypeProtocols504.type_epNoticeApplicationsAbsence) == -1
                                   ]
            list_type_EFInvalidation = [file for file in file_list if
                                        file.find(ClassTypeProtocols.TypeProtocols.type_EFInvalidation) != -1]
            list_type_ProtocolEvasion = [file for file in file_list if
                                         file.find(
                                             ClassTypeProtocols.TypeProtocols.type_ProtocolEvasion) != -1 and file.find(
                                             ClassTypeProtocols504.TypeProtocols504.type_epProtocolEvasion) == -1]
            list_type_OKSingleApp = [file for file in file_list if
                                     file.find(ClassTypeProtocols.TypeProtocols.type_OKSingleApp) != -1]
            list_type_OKDSingleApp = [file for file in file_list if
                                      file.find(ClassTypeProtocols.TypeProtocols.type_OKDSingleApp) != -1]
            list_type_OKOUSingleApp = [file for file in file_list if
                                       file.find(ClassTypeProtocols.TypeProtocols.type_OKOUSingleApp) != -1]
            list_type_ProposalsResult = [file for file in file_list if
                                         file.find(ClassTypeProtocols.TypeProtocols.type_ProtocolProposalsResult) != -1]
            list_type_OK1 = [file for file in file_list if file.find(ClassTypeProtocols.TypeProtocols.type_OK1) != -1]
            list_type_OKD1 = [file for file in file_list if file.find(ClassTypeProtocols.TypeProtocols.type_OKD1) != -1]
            list_type_OKD2 = [file for file in file_list if file.find(ClassTypeProtocols.TypeProtocols.type_OKD2) != -1]
            list_type_OKD3 = [file for file in file_list if file.find(ClassTypeProtocols.TypeProtocols.type_OKD3) != -1]
            list_type_OKD4 = [file for file in file_list if file.find(ClassTypeProtocols.TypeProtocols.type_OKD4) != -1]
            list_type_OKOU1 = [file for file in file_list if
                               file.find(ClassTypeProtocols.TypeProtocols.type_OKOU1) != -1]
            list_type_OKOU2 = [file for file in file_list if
                               file.find(ClassTypeProtocols.TypeProtocols.type_OKOU2) != -1]
            list_type_Cancel = [file for file in file_list if
                                file.find(ClassTypeProtocols.TypeProtocols.type_Cancel) != -1 and file.find(
                                        ClassTypeProtocols504.TypeProtocols504.type_Cancel504) == -1]
            list_type_AddInfoInvalid = [file for file in file_list if
                                        file.find(ClassTypeProtocols504.TypeProtocols504.type_fcsAddInfoInvalid) != -1]
            list_type_AddInfo = [file for file in file_list if
                                 file.find(ClassTypeProtocols504.TypeProtocols504.type_fcsAddInfo) != -1 and file.find(
                                         ClassTypeProtocols504.TypeProtocols504.type_fcsAddInfoInvalid) == -1]
            list_type_pprf615ProtocolEF2 = [file for file in file_list if
                                            file.find(
                                                ClassTypeProtocols504.TypeProtocols504.type_pprf615ProtocolEF2) != -1]
            list_type_pprf615QualifiedContractor = [file for file in file_list if
                                                    file.find(
                                                            ClassTypeProtocols504.TypeProtocols504.type_pprf615QualifiedContractor) != -1]
            list_type_pprf615ProtocolPO = [file for file in file_list if
                                           file.find(
                                                   ClassTypeProtocols504.TypeProtocols504.type_pprf615ProtocolPO) != -1]
            list_type_pprf615ProtocolEF1 = [file for file in file_list if
                                            file.find(
                                                    ClassTypeProtocols504.TypeProtocols504.type_pprf615ProtocolEF1) != -1]
            set_type_Other = (set(file_list) - set(list_type_EF1) - set(list_type_EF2) - set(list_type_EF3) - set(
                    list_type_ZK) \
                             - set(list_type_ZKAfterProlong) - set(list_type_EFSingleApp) - set(list_type_EFSinglePart) \
                             - set(list_type_OK2) - set(list_type_OKD5) - set(list_type_OKOU3) - set(list_type_ZPFinal) \
                             - set(list_type_Deviation) - set(list_type_EFInvalidation) - set(
                    list_type_OKSingleApp) - set(list_type_OKOUSingleApp) \
                             - set(list_type_OK1) - set(list_type_OKD1) - set(list_type_OKD2) - set(list_type_OKD3) \
                             - set(list_type_OKD4) - set(list_type_OKOU1) - set(list_type_OKOU2) - set(list_type_Cancel) \
                              - set(list_type_ProtocolEvasion) - set(list_type_AddInfo) - set(
                        list_type_AddInfoInvalid) - set(list_type_pprf615ProtocolEF2)
                              - set(list_type_pprf615QualifiedContractor) - set(list_type_pprf615ProtocolPO) - set(
                        list_type_pprf615ProtocolEF1))

        except Exception as ex:
            # print('Не удалось получить список файлов ' + str(ex) + ' ' + l_dir)
            logging.exception("Ошибка: ")
            with open(file_log, 'a') as flog:
                flog.write(f'Не удалось получить список файлов {str(ex)} {l_dir}\n')
        else:
            for f1 in list_type_EF1:
                bolter(f1, l_dir, region, ClassTypeProtocols.TypeProtocols.type_EF1)
            for f2 in list_type_EF2:
                bolter(f2, l_dir, region, ClassTypeProtocols.TypeProtocols.type_EF2)
            for f3 in list_type_EF3:
                bolter(f3, l_dir, region, ClassTypeProtocols.TypeProtocols.type_EF3)
            for f4 in list_type_ZK:
                bolter(f4, l_dir, region, ClassTypeProtocols.TypeProtocols.type_ZK)
            for f5 in list_type_ZKAfterProlong:
                bolter(f5, l_dir, region, ClassTypeProtocols.TypeProtocols.type_ZKAfterProlong)
            for f6 in list_type_EFSingleApp:
                bolter(f6, l_dir, region, ClassTypeProtocols.TypeProtocols.type_EFSingleApp)
            for f7 in list_type_OK2:
                bolter(f7, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OK2)
            for f8 in list_type_OKD5:
                bolter(f8, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKD5)
            for f9 in list_type_OKOU3:
                bolter(f9, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKOU3)
            for f10 in list_type_ZPFinal:
                bolter(f10, l_dir, region, ClassTypeProtocols.TypeProtocols.type_ZPFinal)
            for f11 in list_type_EFSinglePart:
                bolter(f11, l_dir, region, ClassTypeProtocols.TypeProtocols.type_EFSinglePart)
            for f12 in list_type_Deviation:
                bolter(f12, l_dir, region, ClassTypeProtocols.TypeProtocols.type_Deviation)
            for f13 in list_type_EFInvalidation:
                bolter(f13, l_dir, region, ClassTypeProtocols.TypeProtocols.type_EFInvalidation)
            for f14 in list_type_OKSingleApp:
                bolter(f14, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKSingleApp)
            for f15 in list_type_OKDSingleApp:
                bolter(f15, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKDSingleApp)
            for f16 in list_type_OKOUSingleApp:
                bolter(f16, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKOUSingleApp)
            for f17 in list_type_OK1:
                bolter(f17, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OK1)
            for f18 in list_type_OKD1:
                bolter(f18, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKD1)
            for f19 in list_type_OKD2:
                bolter(f19, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKD2)
            for f20 in list_type_OKD3:
                bolter(f20, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKD3)
            for f99 in list_type_ProposalsResult:
                bolter(f99, l_dir, region, ClassTypeProtocols.TypeProtocols.type_ProtocolProposalsResult)
            for f21 in list_type_OKD4:
                bolter(f21, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKD4)
            for f22 in list_type_OKOU1:
                bolter(f22, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKOU1)
            for f23 in list_type_OKOU2:
                bolter(f23, l_dir, region, ClassTypeProtocols.TypeProtocols.type_OKOU2)
            for f24 in list_type_Cancel:
                bolter(f24, l_dir, region, ClassTypeProtocols.TypeProtocols.type_Cancel)
            for f26 in list_type_ProtocolEvasion:
                bolter(f26, l_dir, region, ClassTypeProtocols.TypeProtocols.type_ProtocolEvasion)
            for f27 in list_type_AddInfo:
                bolter(f27, l_dir, region, ClassTypeProtocols504.TypeProtocols504.type_fcsAddInfo)
            for f28 in list_type_AddInfoInvalid:
                bolter(f28, l_dir, region, ClassTypeProtocols504.TypeProtocols504.type_fcsAddInfoInvalid)
            for f38 in list_type_pprf615ProtocolEF1:
                bolter(f38, l_dir, region, ClassTypeProtocols504.TypeProtocols504.type_pprf615ProtocolEF1)
            for f29 in list_type_pprf615ProtocolEF2:
                bolter(f29, l_dir, region, ClassTypeProtocols504.TypeProtocols504.type_pprf615ProtocolEF2)
            for f30 in list_type_pprf615QualifiedContractor:
                bolter(f30, l_dir, region, ClassTypeProtocols504.TypeProtocols504.type_pprf615QualifiedContractor)
            for f31 in list_type_pprf615ProtocolPO:
                bolter(f31, l_dir, region, ClassTypeProtocols504.TypeProtocols504.type_pprf615ProtocolPO)
            for f25 in set_type_Other:
                bolter(f25, l_dir, region, None)

        os.remove(l)
        try:
            shutil.rmtree(l_dir, ignore_errors=True)
        except Exception:
            pass


@timeout_decorator.timeout(600)
def down_timeout(m, path_parse1):
    host = 'ftp.zakupki.gov.ru'
    ftpuser = 'free'
    password = 'VNIMANIE!_otkluchenie_FTP_s_01_01_2025_podrobnee_v_ATFF'
    with ftplib.FTP(host) as ftp2:
        ftp2.set_debuglevel(0)
        ftp2.encoding = 'utf8'
        ftp2.login(ftpuser, password)
        ftp2.cwd(path_parse1)
        local_f = '{0}/{1}'.format(TEMP_DIR, str(m))
        lf = open(local_f, 'wb')
        ftp2.retrbinary('RETR ' + str(m), lf.write)
        lf.close()
        return local_f

def parser_propocols(path_array, path_on_ftp):
    for reg in path_array:
        # if int(reg["id"]) != 81:
        #     continue
        if len(sys.argv) == 1:
            print(
                    'Недостаточно параметров для запуска, используйте curr для парсинга текущего месяца и last или prev'
                    ' для '
                    'прошлых')
            exit()
        elif str(sys.argv[1]) == 'last':
            path_parse = 'fcs_regions/' + reg['path'] + '/' + path_on_ftp + '/'
        elif str(sys.argv[1]) == 'curr':
            path_parse = 'fcs_regions/' + reg['path'] + '/' + path_on_ftp + '/currMonth/'
        elif str(sys.argv[1]) == 'prev':
            path_parse = 'fcs_regions/' + reg['path'] + '/' + path_on_ftp + '/prevMonth/'

        try:
            # получаем список архивов
            if str(sys.argv[1]) == 'curr':
                arr_con = get_list_ftp(path_parse, lambda: get_list_ftp_curr(path_parse, reg['path']))
            elif str(sys.argv[1]) == 'last':
                arr_con = get_list_ftp(path_parse, lambda: get_list_ftp_last(path_parse))
            elif str(sys.argv[1]) == 'prev':
                arr_con = get_list_ftp(path_parse, lambda: get_list_ftp_prev(path_parse, reg['path']))
            else:
                arr_con = []
                print('Неверное имя параметра, используйте curr для парсинга текущего месяца и last или prev '
                      'для прошлых')
                exit()
            for j in arr_con:
                try:
                    extract_prot(j, path_parse, reg['conf'])
                except Exception as exc:
                    print('Ошибка в экстракторе и парсере ' + str(exc) + ' ' + j)
                    logging.exception("Ошибка: ")
                    with open(file_log, 'a') as flog:
                        flog.write('Ошибка в экстракторе и парсере ' + str(exc) + ' ' + j + '\n')
                    continue

        except Exception as ex:
            # print('Не удалось получить список архивов ' + str(ex) + ' ' + path_parse)
            if '550 Failed to change directory' in str(ex):
                logging.warning(f"Can not find directory {path_parse}")
                continue
            logging.exception("Ошибка: ")
            with open(file_log, 'a') as flog:
                flog.write(f'Не удалось получить список архивов {str(ex)} {path_parse}\n')
            continue

def get_ar(m, path_parse1):
    """
    :param m: получаем имя архива
    :param path_parse1: получаем путь до архива
    :return: возвращаем локальный путь до архива или 0 в случае неудачи
    """
    retry = True
    count = 0
    while retry:
        try:
            lf = down_timeout(m, path_parse1)
            retry = False
            return lf
        except Exception as ex:
            time.sleep(5)
            # print('Не удалось скачать архив ' + str(ex) + ' ' + m)
            # logging.exception("Ошибка: ")
            # with open(file_log, 'a') as flog:
            #     flog.write('Не удалось скачать архив ' + str(ex) + ' ' + m + '\n')
            if count > 50:
                with open(file_log, 'a') as flog:
                    flog.write(
                        'Не удалось скачать архив за ' + str(count) + ' попыток ' + str(ex) + ' ' + str(m) + '\n')
                return 0
            count += 1

def get_list_ftp(path_parse, lmbd):
    retry = True
    count = 0
    while retry:
        try:
            lf = lmbd()
            retry = False
            return lf
        except Exception as ex:
            time.sleep(5)
            # print('Не удалось скачать архив ' + str(ex) + ' ' + m)
            # logging.exception("Ошибка: ")
            # with open(file_log, 'a') as flog:
            #     flog.write('Не удалось скачать архив ' + str(ex) + ' ' + m + '\n')
            if count > 50:
                with open(file_log, 'a') as flog:
                    flog.write(
                            'Не удалось получить список архивов за ' + str(count) + ' попыток ' + str(
                                ex) + ' ' + path_parse + '\n')
                return []
            count += 1

def main():
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.mkdir(TEMP_DIR)
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    con_region = connect_bd(DB)
    cur_region = con_region.cursor()
    cur_region.execute("""SELECT * FROM region""")
    path_array = cur_region.fetchall()
    cur_region.close()
    con_region.close()

    parser_propocols(path_array, 'protocols')
    parser_propocols(path_array, 'addinfo')
    parser_propocols(path_array, 'pprf615docs/protocols')
    parser_propocols(path_array, 'pprf615docs/qualifiedContractors')

if __name__ == "__main__":
    logging_parser("Начало парсинга")
    main()
    logging_parser('Добавлено EF1', ClassProtocolEF1.ProtocolEF1.add_protocolEF1)
    logging_parser('Обновлено EF1', ClassProtocolEF1.ProtocolEF1.update_protocolEF1)
    logging_parser('Добавлено EF2', ClassProtocolEF2.ProtocolEF2.add_protocolEF2)
    logging_parser('Обновлено EF2', ClassProtocolEF2.ProtocolEF2.update_protocolEF2)
    logging_parser('Добавлено EF3, SingleApp, SinglePart, ProtocolDeviation, EFInvalidation, ProtocolEvasion',
                   ClassProtocolEF3.ProtocolEF3.add_protocolEF3)
    logging_parser('Обновлено EF3, SingleApp, SinglePart, ProtocolDeviation, EFInvalidation, ProtocolEvasion',
                   ClassProtocolEF3.ProtocolEF3.update_protocolEF3)
    logging_parser('Добавлено ZK и ZKProlongation', ClassProtocolZK.ProtocolZK.add_protocolZK)
    logging_parser('Обновлено ZK и ZKProlongation', ClassProtocolZK.ProtocolZK.update_protocolZK)
    logging_parser('Добавлено OKD5, OK2, OKOU3, ProtocolOKSingleApp, ProtocolOKDSingleApp, ProtocolOKOUSingleApp',
                   ClassProtocolOK2.ProtocolOK2.add_protocolOK2)
    logging_parser('Обновлено OKD5, OK2, OKOU3, ProtocolOKSingleApp, ProtocolOKDSingleApp, ProtocolOKOUSingleApp',
                   ClassProtocolOK2.ProtocolOK2.update_protocolOK2)
    logging_parser('Добавлено ZPFinal', ClassProtocolZPFinal.ProtocolZPFinal.add_protocolZPFinal)
    logging_parser('Обновлено ZPFinal', ClassProtocolZPFinal.ProtocolZPFinal.update_protocolZPFinal)
    logging_parser('Добавлено OK1, OKD1, OKD2, OKD3, OKD4, OKOU1, OKOU2', ClassProtocolOK1.ProtocolOK1.add_protocolOK1)
    logging_parser('Обновлено OK1, OKD1, OKD2, OKD3, OKD4, OKOU1, OKOU2',
                   ClassProtocolOK1.ProtocolOK1.update_protocolOK1)
    logging_parser('Добавлено Cancel', ClassProtocolCancel.ProtocolCancel.add_protocolCancel)
    logging_parser('Обновлено Cancel', ClassProtocolCancel.ProtocolCancel.update_protocolCancel)
    logging_parser('Добавлено EZK1, EZK2', ClassProtocolEZK2.ProtocolEZK2.add_protocolEZK2)
    logging_parser('Обновлено EZK1, EZK2', ClassProtocolEZK2.ProtocolEZK2.update_protocolEZK2)
    logging_parser('Добавлено EOK1, EOKD1, EZP1Extract', ClassProtocolEOK1.ProtocolEOK1.add_protocolEOK1)
    logging_parser('Обновлено EOK1, EOKD1, EZP1Extract', ClassProtocolEOK1.ProtocolEOK1.update_protocolEOK1)
    logging_parser('Добавлено EOK2', ClassProtocolEOK2.ProtocolEOK2.add_protocolEOK2)
    logging_parser('Обновлено EOK2', ClassProtocolEOK2.ProtocolEOK2.update_protocolEOK2)
    logging_parser('Добавлено EZP1', ClassProtocolEZP1.ProtocolEZP1.add_protocolEZP1)
    logging_parser('Обновлено EZP1', ClassProtocolEZP1.ProtocolEZP1.update_protocolEZP1)
    logging_parser('Добавлено EZP2', ClassProtocolEZP2.ProtocolEZP2.add_protocolEZP2)
    logging_parser('Обновлено EZP2', ClassProtocolEZP2.ProtocolEZP2.update_protocolEZP2)
    logging_parser('Добавлено EOK3', ClassProtocolEOK3.ProtocolEOK3.add_protocolEOK3)
    logging_parser('Обновлено EOK3', ClassProtocolEOK3.ProtocolEOK3.update_protocolEOK3)
    logging_parser('Добавлено ProposalsResult', ProtocolProposalsResult.add)
    logging_parser('Обновлено ProposalsResult', ProtocolProposalsResult.update)
    logging_parser('Добавлено Cancel504, epNoticeApplicationCancel, epProtocolEvDevCancel',
                   ClassProtocolCancel504.ProtocolCancel504.add_protocolCancel)
    logging_parser('Обновлено Cancel504, epNoticeApplicationCancel, epProtocolEvDevCancel',
                   ClassProtocolCancel504.ProtocolCancel504.update_protocolCancel)
    logging_parser(
            'Добавлено EOKOU1, EOKSingleApp, EOKSinglePart, EOKOUSingleApp, EOKOUSinglePart, EOKDSingleApp, EOKD2, EOKDSinglePart',
            ClassProtocolEOKOU1.ProtocolEOKOU1.add_protocolEOKOU1)
    logging_parser(
            'Обновлено EOKOU1, EOKSingleApp, EOKSinglePart, EOKOUSingleApp, EOKOUSinglePart, EOKDSingleApp, EOKD2, EOKDSinglePart',
            ClassProtocolEOKOU1.ProtocolEOKOU1.update_protocolEOKOU1)
    logging_parser('Добавлено epProtocolEF2020Final',
                   ClassProtocolEF2020Final.ProtocolEF2020Final.add_protocolEF2020Final)
    logging_parser('Обновлено epProtocolEF2020Final',
                   ClassProtocolEF2020Final.ProtocolEF2020Final.update_protocolEF2020Final)
    logging_parser('Добавлено ProtocolEOKOUSingleApp',
                   ClassProtocolEOKOUSingleApp.ProtocolEOKOUSingleApp.add_protocolEOKOUSingleApp)
    logging_parser('Обновлено ProtocolEOKOUSingleApp',
                   ClassProtocolEOKOUSingleApp.ProtocolEOKOUSingleApp.update_protocoEOKOUSingleApp)
    logging_parser('Добавлено EFSinglePart',
                   ClassProtocolEFSinglePart.ProtocolEFSinglePart.add_protocolEFSinglePart)
    logging_parser('Обновлено EFSinglePart',
                   ClassProtocolEFSinglePart.ProtocolEFSinglePart.update_protocolEFSinglePart)
    logging_parser('Добавлено epProtocolEZK2020FinalPart, epProtocolEZK2020Final',
                   ProtocolEZK2020FinalPart.add_protocolEZK2020FinalPart)
    logging_parser('Обновлено epProtocolEZK2020FinalPart, epProtocolEZK2020Final',
                   ProtocolEZK2020FinalPart.update_protocolEZK2020FinalPart)
    logging_parser('Добавлено epProtocolEF2020SubmitOffers',
                   ProtocolEF2020SubmitOffers.add)
    logging_parser('Обновлено epProtocolEF2020SubmitOffers',
                   ProtocolEF2020SubmitOffers.update)
    logging_parser('Добавлено epProtocolEOK2020SecondSections, epProtocolEOK2020FirstSections',
                   ProtocolEOK2020SecondSections.add)
    logging_parser('Обновлено epProtocolEOK2020SecondSections, epProtocolEOK2020FirstSections',
                   ProtocolEOK2020SecondSections.update)
    logging_parser('Добавлено epProtocolEOK2020Final',
                   ProtocolEOK2020Final.add)
    logging_parser('Обновлено epProtocolEOK2020Final',
                   ProtocolEOK2020Final.update)
    logging_parser('Добавлено epProtocolDeviation, epProtocolDeviation, epProtocolEvasion',
                   ProtocolDeviation.add)
    logging_parser('Обновлено epProtocolDeviation, epProtocolDeviation, epProtocolEvasion',
                   ProtocolDeviation.update)
    logging_parser('Добавлено fcsProtocolVPP',
                   ProtocolEZP1Extract.add)
    logging_parser('Обновлено fcsProtocolVPP',
                   ProtocolEZP1Extract.update)
    logging_parser('Добавлено EOKOU2', ClassProtocolEOKOU2.ProtocolEOKOU2.add_protocolEOKOU2)
    logging_parser('Обновлено EOKOU2', ClassProtocolEOKOU2.ProtocolEOKOU2.update_protocolEOKOU2)
    logging_parser('Добавлено EOKOU3, EOKD4, EOKD3', ClassProtocolEOKOU3.ProtocolEOKOU3.add_protocolEOKOU3)
    logging_parser('Обновлено EOKOU3, EOKD4, EOKD3', ClassProtocolEOKOU3.ProtocolEOKOU3.update_protocolEOKOU3)
    logging_parser('Добавлено pprf615ProtocolEF1', Pprf615ProtocolEF1.add)
    logging_parser('Обновлено pprf615ProtocolEF1', Pprf615ProtocolEF1.update)
    logging_parser('Добавлено epProtocolEZT2020Final', ProtocolEZT2020Final.add)
    logging_parser('Обновлено epProtocolEZT2020Final', ProtocolEZT2020Final.update)
    logging_parser(
            'Добавлено EOKOU1',
            ProtocolEOKOU1New.add)
    logging_parser(
            'Обновлено EOKOU1',
            ProtocolEOKOU1New.update)
    logging_parser(
            'Добавлено AddInfo',
            ProtocolAddInfo.add)
    logging_parser(
            'Обновлено AddInfo',
            ProtocolAddInfo.update)
    logging_parser(
            'Добавлено AddInfoInvalid',
            ProtocolAddInfoInvalid.add)
    logging_parser(
            'Обновлено AddInfoInvalid',
            ProtocolAddInfoInvalid.update)
    logging_parser('Добавлено pprf615ProtocolEF2', Pprf615ProtocolEF2.add)
    logging_parser('Обновлено pprf615ProtocolEF2', Pprf615ProtocolEF2.update)
    logging_parser('Добавлено pprf615QualifiedContractor', Pprf615QualifiedContractor.add)
    logging_parser('Обновлено pprf615QualifiedContractor', Pprf615QualifiedContractor.update)
    logging_parser('Добавлено pprf615ProtocolPO', Pprf615ProtocolPO.add)
    logging_parser('Обновлено pprf615ProtocolPO', Pprf615ProtocolPO.update)
    logging_parser("Конец парсинга")
