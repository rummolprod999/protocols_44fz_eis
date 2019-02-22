import datetime
import logging
import operator
import traceback
from functools import reduce
from warnings import filterwarnings
import dateutil.parser
import os
import pymysql

from connect_to_db import connect_bd
from parser_prot_class import Type_protocol, Type_protocol504, ProtocolEZK2, ProtocolEZP2
from ClassProtocolEZP1 import ProtocolEZP1
from ClassProtocolEOK1 import ProtocolEOK1
from ClassProtocolEOK2 import ProtocolEOK2
from ClassProtocolCancel import ProtocolCancel
from ClassProtocolOK1 import ProtocolOK1
from ClassProtocolOK2 import ProtocolOK2
from ClassProtocolZK import ProtocolZK
from ClassProtocolZPFinal import ProtocolZPFinal
from ClassProtocolEF3 import ProtocolEF3
from ClassProtocolEF1 import ProtocolEF1
from ClassProtocolEF2 import ProtocolEF2

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


def logging_parser(*kwargs):
    s_log = f'{datetime.datetime.now()} '
    for i in kwargs:
        s_log += f'{i} '
    s_log += '\n\n'
    with open(file_log, 'a') as flog:
        flog.write(s_log)


def check_yeld(h) -> bool:
    flag = False
    for i in h:
        if i:
            flag = True
    return flag


def get_from_dict(data_dict, map_list):
    return reduce(operator.getitem, map_list, data_dict)


def generator_univ(c):
    if c == "":
        raise StopIteration
    if type(c) == list:
        for i in c:
            yield i
    else:
        yield c


def get_el(d, *kwargs):
    try:
        res = get_from_dict(d, kwargs)
    except Exception:
        res = ''
    if res is None:
        res = ''
    if type(res) is str:
        res = res.strip()
    return res


def get_el_list(d, *kwargs):
    try:
        res = get_from_dict(d, kwargs)
    except Exception:
        res = []
    if res is None:
        res = []
    return res


def parserEF1(doc, path_xml, filexml, reg, type_f):
    p = ProtocolEF1(doc, filexml)
    id_p = 0
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    abandoned_reason_name = p.get_abandoned_reason_name()
    con = connect_bd(DB)
    cur = con.cursor()
    cur.execute(f"""SELECT id FROM {PREFIX}auction_start_protocol WHERE id_protocol = %s AND purchase_number = %s 
                    AND type_protocol = %s""",
                (id_protocol, purchase_number, type_f))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_start_protocol WHERE purchase_number = %s 
                    AND type_protocol = %s""",
                (purchase_number, type_f))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot > datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_start_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_start_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                    url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, abandoned_reason_name = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
             abandoned_reason_name))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolEF1.update_protocolEF1 += 1
    else:
        ProtocolEF1.add_protocolEF1 += 1
    for app in p.applications:
        journal_number = p.get_journal_number(app)
        admission = p.get_admission(app)
        cur.execute(
                f"""INSERT INTO {PREFIX}auction_start_applications SET id_auction_protocol = %s, 
                    journal_number = %s, 
                    admission = %s""",
                (
                    id_p, journal_number, admission))
    cur.close()
    con.close()


def parserEF2(doc, path_xml, filexml, reg, type_f):
    p = ProtocolEF2(doc, filexml)
    id_p = 0
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    con = connect_bd(DB)
    cur = con.cursor()
    cur.execute(f"""SELECT id FROM {PREFIX}auction_protocol WHERE id_protocol = %s AND purchase_number = %s 
                AND type_protocol = %s""",
                (id_protocol, purchase_number, type_f))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_protocol WHERE purchase_number = %s 
                AND type_protocol = %s""",
                (purchase_number, type_f))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot > datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolEF2.update_protocolEF2 += 1
    else:
        ProtocolEF2.add_protocolEF2 += 1
    for app in p.applications:
        journal_number = p.get_journal_number(app)
        offer_first_price = p.get_offer_first_price(app)
        offer_last_price = p.get_offer_last_price(app)
        offer_quantity = p.get_offer_quantity(app)
        cur.execute(
                f"""INSERT INTO {PREFIX}auction_applications SET id_auction_protocol = %s, 
                    journal_number = %s, 
                    offer_first_price = %s, offer_last_price = %s, offer_quantity = %s""",
                (
                    id_p, journal_number, offer_first_price,
                    offer_last_price,
                    offer_quantity))
    cur.close()
    con.close()


def parserEF3(doc, path_xml, filexml, reg, type_f):
    p = ProtocolEF3(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    abandoned_reason_name = p.get_abandoned_reason_name()
    lot_number = 1
    con = connect_bd(DB)
    cur = con.cursor()
    cur.execute(
            f"""SELECT id FROM {PREFIX}auction_end_protocol WHERE id_protocol = %s AND purchase_number = %s 
            AND type_protocol = %s""",
            (id_protocol, purchase_number, type_f))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    ref_fact = p.get_refusalFact_name()
    if ref_fact:
        cancel_status = 1
    ref_fact = f"{ref_fact} {p.get_ref_explation()}".strip()
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_end_protocol WHERE purchase_number = %s 
                AND type_protocol = %s""",
                (purchase_number, type_f))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_end_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_end_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                    url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, abandoned_reason_name = %s, lot_number = %s, refusal_fact = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
             abandoned_reason_name, lot_number, ref_fact))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolEF3.update_protocolEF3 += 1
    else:
        ProtocolEF3.add_protocolEF3 += 1
    for app in p.applications:
        id_participiant = 0
        journal_number = p.get_journal_number(app)
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_post_address(app)
        if inn:
            cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                        (inn, kpp))
            res_p = cur.fetchone()
            if res_p:
                id_participiant = res_p['id']
            else:
                cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                        organization_name = %s, participant_type = %s, country_full_name = %s, 
                        post_address = %s""",
                            (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                id_participiant = cur.lastrowid
        if id_participiant == 0:
            logging_parser('Нет инн', xml, type_f)
        app_rating = p.get_app_rating(app)
        admission = p.get_admission(app)
        cur.execute(f"""INSERT INTO {PREFIX}auction_end_applications SET id_auction_end_protocol = %s, 
                        journal_number = %s, app_rating = %s, admission = %s, 
                        id_participiant = %s""",
                    (id_p, journal_number, app_rating,
                     admission, id_participiant))
    cur.close()
    con.close()


def parserZK(doc, path_xml, filexml, reg, type_f):
    p = ProtocolZK(doc, path_xml)
    # p.test_abandoned_reason_name()
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    abandoned_reason_name = p.get_abandoned_reason_name()
    lot_number = p.get_lot_number()
    con = connect_bd(DB)
    cur = con.cursor()
    cur.execute(
            f"""SELECT id FROM {PREFIX}auction_end_protocol WHERE id_protocol = %s AND purchase_number = %s 
            AND type_protocol = %s AND lot_number = %s""",
            (id_protocol, purchase_number, type_f, lot_number))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_end_protocol WHERE purchase_number = %s 
                    AND type_protocol = %s AND lot_number = %s""",
                (purchase_number, type_f, lot_number))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_end_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_end_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                        url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, 
                        abandoned_reason_name = %s, lot_number = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
             abandoned_reason_name, lot_number))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolZK.update_protocolZK += 1
    else:
        ProtocolZK.add_protocolZK += 1
    for app in p.applications:
        id_participiant = 0
        journal_number = p.get_journal_number(app)
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_post_address(app)
        if inn:
            cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                        (inn, kpp))
            res_p = cur.fetchone()
            if res_p:
                id_participiant = res_p['id']
            else:
                cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                        organization_name = %s, participant_type = %s, country_full_name = %s, 
                        post_address = %s""",
                            (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                id_participiant = cur.lastrowid
        if id_participiant == 0:
            logging_parser('Нет инн', xml, type_f)
        result_zk = p.get_result_zk(app)
        price_zk = p.get_price(app)
        cur.execute(f"""INSERT INTO {PREFIX}auction_end_applications SET id_auction_end_protocol = %s, 
                        journal_number = %s, result_zk = %s, price = %s, 
                        id_participiant = %s""",
                    (id_p, journal_number, result_zk,
                     price_zk, id_participiant))
    cur.close()
    con.close()


def parserOK2(doc, path_xml, filexml, reg, type_f):
    p = ProtocolOK2(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    con = connect_bd(DB)
    cur = con.cursor()
    for lot in p.lots:
        lot_number = p.get_lot_number(lot)
        abandoned_reason_name = p.get_abandoned_reason_name(lot)
        cur.execute(
                f"""SELECT id FROM {PREFIX}auction_end_protocol WHERE id_protocol = %s AND purchase_number = %s 
                AND type_protocol = %s AND lot_number = %s""",
                (id_protocol, purchase_number, type_f, lot_number))
        res_id = cur.fetchone()
        if res_id:
            # logging_parser('такой протокол есть в базе', xml)
            cur.close()
            con.close()
            return
        cancel_status = 0
        updated = False
        date_prot = dateutil.parser.parse(protocol_date[:19])
        cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_end_protocol WHERE purchase_number = %s 
                            AND type_protocol = %s AND lot_number = %s""",
                    (purchase_number, type_f, lot_number))
        res_prot = cur.fetchall()
        if res_prot:
            updated = True
            for r in res_prot:
                if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                    cur.execute(f"""UPDATE {PREFIX}auction_end_protocol SET cancel = 1 WHERE id = %s""",
                                (r['id'],))
                else:
                    cancel_status = 1
        cur.execute(
                f"""INSERT INTO {PREFIX}auction_end_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                                url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, abandoned_reason_name = %s, 
                                lot_number = %s""",
                (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
                 abandoned_reason_name, lot_number))
        id_p = cur.lastrowid
        if not id_p:
            logging_parser('Не получили id', xml)
        if updated:
            ProtocolOK2.update_protocolOK2 += 1
        else:
            ProtocolOK2.add_protocolOK2 += 1
        applications = p.get_applications(lot)
        for app in applications:
            journal_number = p.get_journal_number(app)
            app_rating = p.get_app_rating(app)
            participiants = p.get_participiants(app)
            admission = p.get_admission(app)
            for part in participiants:
                id_participiant = 0
                inn = p.get_inn(part)
                kpp = p.get_kpp(part)
                organization_name = p.get_organization_name(part)
                participant_type = p.get_participant_type(part)
                country_full_name = p.get_country_full_name(part)
                post_address = p.get_post_address(part)
                if inn:
                    cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                                (inn, kpp))
                    res_p = cur.fetchone()
                    if res_p:
                        id_participiant = res_p['id']
                    else:
                        cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                                            organization_name = %s, participant_type = %s, country_full_name = %s, 
                                            post_address = %s""",
                                    (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                        id_participiant = cur.lastrowid
                if id_participiant == 0:
                    logging_parser('Нет инн', xml, type_f)

                cur.execute(f"""INSERT INTO {PREFIX}auction_end_applications SET id_auction_end_protocol = %s, 
                                            journal_number = %s, app_rating = %s, admission = %s,
                                            id_participiant = %s""",
                            (id_p, journal_number, app_rating, admission, id_participiant))

    cur.close()
    con.close()


def parserZPFinal(doc, path_xml, filexml, reg, type_f):
    p = ProtocolZPFinal(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    lot_number = 1
    con = connect_bd(DB)
    cur = con.cursor()
    cur.execute(
            f"""SELECT id FROM {PREFIX}auction_end_protocol WHERE id_protocol = %s AND purchase_number = %s 
            AND type_protocol = %s""",
            (id_protocol, purchase_number, type_f))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_end_protocol WHERE purchase_number = %s 
                    AND type_protocol = %s""",
                (purchase_number, type_f))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_end_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_end_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                        url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, lot_number = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status, lot_number))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolZPFinal.update_protocolZPFinal += 1
    else:
        ProtocolZPFinal.add_protocolZPFinal += 1
    for app in p.applications:
        id_participiant = 0
        journal_number = p.get_journal_number(app)
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_post_address(app)
        if inn:
            cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                        (inn, kpp))
            res_p = cur.fetchone()
            if res_p:
                id_participiant = res_p['id']
            else:
                cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                            organization_name = %s, participant_type = %s, country_full_name = %s, 
                            post_address = %s""",
                            (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                id_participiant = cur.lastrowid
        if id_participiant == 0:
            logging_parser('Нет инн', xml, type_f)
        app_rating = p.get_app_rating(app)
        admission = p.get_admission(app)
        price = p.get_price(app)
        cur.execute(f"""INSERT INTO {PREFIX}auction_end_applications SET id_auction_end_protocol = %s, 
                            journal_number = %s, app_rating = %s, admission = %s, 
                            id_participiant = %s, price = %s""",
                    (id_p, journal_number, app_rating,
                     admission, id_participiant, price))
    cur.close()
    con.close()


def parserOK1(doc, path_xml, filexml, reg, type_f):
    p = ProtocolOK1(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    # print(purchase_number)
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    con = connect_bd(DB)
    cur = con.cursor()
    for lot in p.lots:
        lot_number = p.get_lot_number(lot)
        abandoned_reason_name = p.get_abandoned_reason_name(lot)
        cur.execute(
                f"""SELECT id FROM {PREFIX}auction_start_protocol WHERE id_protocol = %s AND purchase_number = %s 
                AND type_protocol = %s AND lot_number = %s""",
                (id_protocol, purchase_number, type_f, lot_number))
        res_id = cur.fetchone()
        if res_id:
            # logging_parser('такой протокол есть в базе', xml)
            cur.close()
            con.close()
            return
        cancel_status = 0
        updated = False
        date_prot = dateutil.parser.parse(protocol_date[:19])
        cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_start_protocol WHERE purchase_number = %s 
                                AND type_protocol = %s AND lot_number = %s""",
                    (purchase_number, type_f, lot_number))
        res_prot = cur.fetchall()
        if res_prot:
            updated = True
            for r in res_prot:
                if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                    cur.execute(f"""UPDATE {PREFIX}auction_start_protocol SET cancel = 1 WHERE id = %s""",
                                (r['id'],))
                else:
                    cancel_status = 1
        cur.execute(
                f"""INSERT INTO {PREFIX}auction_start_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                                    url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, abandoned_reason_name = %s, 
                                    lot_number = %s""",
                (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
                 abandoned_reason_name, lot_number))
        id_p = cur.lastrowid
        if not id_p:
            logging_parser('Не получили id', xml)
        if updated:
            ProtocolOK1.update_protocolOK1 += 1
        else:
            ProtocolOK1.add_protocolOK1 += 1
        applications = p.get_applications(lot)
        for app in applications:
            journal_number = p.get_journal_number(app)
            participiants = p.get_participiants(app)
            admission = p.get_admission(app)
            for part in participiants:
                id_participiant = 0
                inn = p.get_inn(part)
                kpp = p.get_kpp(part)
                organization_name = p.get_organization_name(part)
                participant_type = p.get_participant_type(part)
                country_full_name = p.get_country_full_name(part)
                post_address = p.get_post_address(part)
                if inn:
                    cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                                (inn, kpp))
                    res_p = cur.fetchone()
                    if res_p:
                        id_participiant = res_p['id']
                    else:
                        cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                                                organization_name = %s, participant_type = %s, country_full_name = %s, 
                                                post_address = %s""",
                                    (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                        id_participiant = cur.lastrowid
                if id_participiant == 0:
                    logging_parser('Нет инн', xml, type_f)

                cur.execute(f"""INSERT INTO {PREFIX}auction_start_applications SET id_auction_protocol = %s, 
                                                journal_number = %s, admission = %s,
                                                id_participiant = %s""",
                            (id_p, journal_number, admission, id_participiant))

    cur.close()
    con.close()


def parserCancel(doc, path_xml, filexml, reg, type_f):
    p = ProtocolCancel(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    # print(purchase_number)
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    protocol_number = p.get_protocol_number()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    authority_name = p.get_authority_name()
    doc_name = p.get_doc_name()
    con = connect_bd(DB)
    cur = con.cursor()
    cur.execute(f"""SELECT id FROM {PREFIX}auction_protocol_cancel WHERE id_protocol = %s AND purchase_number = %s 
                        AND protocol_number = %s""",
                (id_protocol, purchase_number, protocol_number))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(
            f"""SELECT id, protocol_date FROM {PREFIX}auction_protocol_cancel WHERE purchase_number = %s AND protocol_number = %s""",
            (purchase_number, protocol_number))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot > datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_start_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_protocol_cancel SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                        url = %s, print_form = %s, xml = %s, protocol_number = %s, cancel = %s, authority_name = %s, doc_name = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, protocol_number, cancel_status,
             authority_name, doc_name))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolCancel.update_protocolCancel += 1
    else:
        ProtocolCancel.add_protocolCancel += 1
    cur.close()
    con.close()


def parserEOK1(doc, path_xml, filexml, reg, type_f):
    p = ProtocolEOK1(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    # print(purchase_number)
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    con = connect_bd(DB)
    cur = con.cursor()
    lot_number = 1
    abandoned_reason_name = p.get_abandoned_reason_name()
    cur.execute(
            f"""SELECT id FROM {PREFIX}auction_start_protocol WHERE id_protocol = %s AND purchase_number = %s 
            AND type_protocol = %s AND lot_number = %s""",
            (id_protocol, purchase_number, type_f, lot_number))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_start_protocol WHERE purchase_number = %s 
                                   AND type_protocol = %s AND lot_number = %s""",
                (purchase_number, type_f, lot_number))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_start_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_start_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                                       url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, abandoned_reason_name = %s, 
                                       lot_number = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
             abandoned_reason_name, lot_number))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolEOK1.update_protocolEOK1 += 1
    else:
        ProtocolEOK1.add_protocolEOK1 += 1
    for app in p.applications:
        journal_number = p.get_journal_number(app)
        admission = p.get_admission(app)
        id_participiant = 0
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_post_address(app)
        if inn:
            cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                        (inn, kpp))
            res_p = cur.fetchone()
            if res_p:
                id_participiant = res_p['id']
            else:
                cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                                                   organization_name = %s, participant_type = %s, country_full_name = %s, 
                                                   post_address = %s""",
                            (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                id_participiant = cur.lastrowid

        cur.execute(f"""INSERT INTO {PREFIX}auction_start_applications SET id_auction_protocol = %s, 
                                                   journal_number = %s, admission = %s,
                                                   id_participiant = %s""",
                    (id_p, journal_number, admission, id_participiant))
    cur.close()
    con.close()


def parserEZP1(doc, path_xml, filexml, reg, type_f):
    p = ProtocolEZP1(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    # print(purchase_number)
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    con = connect_bd(DB)
    cur = con.cursor()
    lot_number = 1
    abandoned_reason_name = p.get_abandoned_reason_name()
    cur.execute(
            f"""SELECT id FROM {PREFIX}auction_start_protocol WHERE id_protocol = %s AND purchase_number = %s 
            AND type_protocol = %s AND lot_number = %s""",
            (id_protocol, purchase_number, type_f, lot_number))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_start_protocol WHERE purchase_number = %s 
                                   AND type_protocol = %s AND lot_number = %s""",
                (purchase_number, type_f, lot_number))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_start_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_start_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                                       url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, abandoned_reason_name = %s, 
                                       lot_number = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
             abandoned_reason_name, lot_number))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolEZP1.update_protocolEZP1 += 1
    else:
        ProtocolEZP1.add_protocolEZP1 += 1
    for app in p.applications:
        journal_number = p.get_journal_number(app)
        admission = p.get_admission(app)
        id_participiant = 0
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_post_address(app)
        if inn:
            cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                        (inn, kpp))
            res_p = cur.fetchone()
            if res_p:
                id_participiant = res_p['id']
            else:
                cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                                                   organization_name = %s, participant_type = %s, country_full_name = %s, 
                                                   post_address = %s""",
                            (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                id_participiant = cur.lastrowid

        cur.execute(f"""INSERT INTO {PREFIX}auction_start_applications SET id_auction_protocol = %s, 
                                                   journal_number = %s, admission = %s,
                                                   id_participiant = %s""",
                    (id_p, journal_number, admission, id_participiant))
    cur.close()
    con.close()


def parserEZK2(doc, path_xml, filexml, reg, type_f):
    p = ProtocolEZK2(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    abandoned_reason_name = p.get_abandoned_reason_name()
    lot_number = p.get_lot_number()
    con = connect_bd(DB)
    cur = con.cursor()
    cur.execute(
            f"""SELECT id FROM {PREFIX}auction_end_protocol WHERE id_protocol = %s AND purchase_number = %s 
            AND type_protocol = %s AND lot_number = %s""",
            (id_protocol, purchase_number, type_f, lot_number))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_end_protocol WHERE purchase_number = %s 
                        AND type_protocol = %s AND lot_number = %s""",
                (purchase_number, type_f, lot_number))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_end_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_end_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                            url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, 
                            abandoned_reason_name = %s, lot_number = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
             abandoned_reason_name, lot_number))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolEZK2.update_protocolEZK2 += 1
    else:
        ProtocolEZK2.add_protocolEZK2 += 1
    for app in p.applications:
        id_participiant = 0
        journal_number = p.get_journal_number(app)
        admission = p.get_admission(app)
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_post_address(app)
        if inn:
            cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                        (inn, kpp))
            res_p = cur.fetchone()
            if res_p:
                id_participiant = res_p['id']
            else:
                cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                            organization_name = %s, participant_type = %s, country_full_name = %s, 
                            post_address = %s""",
                            (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                id_participiant = cur.lastrowid
        if id_participiant == 0:
            logging_parser('Нет инн', xml, type_f)
        result_zk = p.get_result_zk(app)
        price_zk = p.get_price(app)
        cur.execute(f"""INSERT INTO {PREFIX}auction_end_applications SET id_auction_end_protocol = %s, 
                            journal_number = %s, result_zk = %s, price = %s, 
                            id_participiant = %s, admission = %s""",
                    (id_p, journal_number, result_zk,
                     price_zk, id_participiant, admission))
    cur.close()
    con.close()


def parserEOK2(doc, path_xml, filexml, reg, type_f):
    p = ProtocolEOK2(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    con = connect_bd(DB)
    cur = con.cursor()
    lot_number = 1
    abandoned_reason_name = p.get_abandoned_reason_name()
    cur.execute(
            f"""SELECT id FROM {PREFIX}auction_end_protocol WHERE id_protocol = %s AND purchase_number = %s 
            AND type_protocol = %s AND lot_number = %s""",
            (id_protocol, purchase_number, type_f, lot_number))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_end_protocol WHERE purchase_number = %s 
                            AND type_protocol = %s AND lot_number = %s""",
                (purchase_number, type_f, lot_number))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_end_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_end_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                                url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, abandoned_reason_name = %s, 
                                lot_number = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
             abandoned_reason_name, lot_number))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolEOK2.update_protocolEOK2 += 1
    else:
        ProtocolEOK2.add_protocolEOK2 += 1
    for app in p.applications:
        journal_number = p.get_journal_number(app)
        app_rating = p.get_app_rating(app)
        admission = p.get_admission(app)
        id_participiant = 0
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_post_address(app)
        if inn:
            cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                        (inn, kpp))
            res_p = cur.fetchone()
            if res_p:
                id_participiant = res_p['id']
            else:
                cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                                            organization_name = %s, participant_type = %s, country_full_name = %s, 
                                            post_address = %s""",
                            (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                id_participiant = cur.lastrowid
        if id_participiant == 0:
            logging_parser('Нет инн', xml, type_f)

        cur.execute(f"""INSERT INTO {PREFIX}auction_end_applications SET id_auction_end_protocol = %s, 
                                            journal_number = %s, app_rating = %s, admission = %s,
                                            id_participiant = %s""",
                    (id_p, journal_number, app_rating, admission, id_participiant))
    cur.close()
    con.close()


def parserEZP1Extract(doc, path_xml, filexml, reg, type_f):
    # TODO
    pass


def parserEZP2(doc, path_xml, filexml, reg, type_f):
    p = ProtocolEZP2(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form()
    protocol_date = p.get_protocol_date()
    lot_number = 1
    abandoned_reason_name = p.get_abandoned_reason_name()
    con = connect_bd(DB)
    cur = con.cursor()
    cur.execute(
            f"""SELECT id FROM {PREFIX}auction_end_protocol WHERE id_protocol = %s AND purchase_number = %s 
                AND type_protocol = %s""",
            (id_protocol, purchase_number, type_f))
    res_id = cur.fetchone()
    if res_id:
        # logging_parser('такой протокол есть в базе', xml)
        cur.close()
        con.close()
        return
    cancel_status = 0
    updated = False
    date_prot = dateutil.parser.parse(protocol_date[:19])
    cur.execute(f"""SELECT id, protocol_date FROM {PREFIX}auction_end_protocol WHERE purchase_number = %s 
                        AND type_protocol = %s""",
                (purchase_number, type_f))
    res_prot = cur.fetchall()
    if res_prot:
        updated = True
        for r in res_prot:
            if date_prot >= datetime.datetime.strptime(str(r['protocol_date']), "%Y-%m-%d %H:%M:%S"):
                cur.execute(f"""UPDATE {PREFIX}auction_end_protocol SET cancel = 1 WHERE id = %s""",
                            (r['id'],))
            else:
                cancel_status = 1
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_end_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                            url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, lot_number = %s,  abandoned_reason_name = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status, lot_number,
             abandoned_reason_name))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolEZP2.update_protocolEZP2 += 1
    else:
        ProtocolEZP2.add_protocolEZP2 += 1
    for app in p.applications:
        id_participiant = 0
        journal_number = p.get_journal_number(app)
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_post_address(app)
        if inn:
            cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE inn = %s AND kpp = %s""",
                        (inn, kpp))
            res_p = cur.fetchone()
            if res_p:
                id_participiant = res_p['id']
            else:
                cur.execute(f"""INSERT INTO {PREFIX}auction_participant SET inn = %s, kpp = %s, 
                                organization_name = %s, participant_type = %s, country_full_name = %s, 
                                post_address = %s""",
                            (inn, kpp, organization_name, participant_type, country_full_name, post_address))
                id_participiant = cur.lastrowid
        if id_participiant == 0:
            logging_parser('Нет инн', xml, type_f)
        app_rating = p.get_app_rating(app)
        admission = p.get_admission(app)
        price = p.get_price(app)
        cur.execute(f"""INSERT INTO {PREFIX}auction_end_applications SET id_auction_end_protocol = %s, 
                                journal_number = %s, app_rating = %s, admission = %s, 
                                id_participiant = %s, price = %s""",
                    (id_p, journal_number, app_rating,
                     admission, id_participiant, price))
    cur.close()
    con.close()


def parserOther(doc, path_xml, filexml, reg, type_f):
    prot = doc[list(doc.keys())[0]]
    list_p = [v for v in prot.keys() if v.lower().startswith("ep")]
    if len(list_p) == 0:
        logging_parser("Can not find protocol tag", filexml)
        return
    if list_p[0] == Type_protocol504.type_EZP1:
        parserEZP1(doc, path_xml, filexml, reg, Type_protocol504.type_EZP1)
        pass
    elif list_p[0] == Type_protocol504.type_EOK2:
        parserEOK2(doc, path_xml, filexml, reg, Type_protocol504.type_EOK2)
        pass
    elif list_p[0] == Type_protocol504.type_EOK1:
        parserEOK1(doc, path_xml, filexml, reg, Type_protocol504.type_EOK1)
        pass
    elif list_p[0] == Type_protocol504.type_EZK2:
        parserEZK2(doc, path_xml, filexml, reg, Type_protocol504.type_EZK2)
        pass
    elif list_p[0] == Type_protocol504.type_EZK1:
        parserEZK2(doc, path_xml, filexml, reg, Type_protocol504.type_EZK1)
        pass
    elif list_p[0] == Type_protocol504.type_EZP1Extract:
        parserEZP1Extract(doc, path_xml, filexml, reg, Type_protocol504.type_EZP1Extract)
        pass
    if list_p[0] == Type_protocol504.type_EZP2:
        parserEZP2(doc, path_xml, filexml, reg, Type_protocol504.type_EZP2)
        pass
    else:
        logging_parser("New type protocol", list_p[0], path_xml)


def parser(doc, path_xml, filexml, reg, type_f):
    global file_log
    try:
        if type_f == Type_protocol.type_EF1:
            parserEF1(doc, path_xml, filexml, reg, type_f)
            pass
        elif type_f == Type_protocol.type_EF2:
            pass
            parserEF2(doc, path_xml, filexml, reg, type_f)
        elif (type_f == Type_protocol.type_EF3 or type_f == Type_protocol.type_EFSingleApp or
              type_f == Type_protocol.type_EFSinglePart or type_f == Type_protocol.type_Deviation or
              type_f == Type_protocol.type_EFInvalidation):
            pass
            parserEF3(doc, path_xml, filexml, reg, type_f)
        elif type_f == Type_protocol.type_ZK or type_f == Type_protocol.type_ZKAfterProlong:
            pass
            parserZK(doc, path_xml, filexml, reg, type_f)
        elif (type_f == Type_protocol.type_OK2 or type_f == Type_protocol.type_OKD5 or
              type_f == Type_protocol.type_OKOU3 or type_f == Type_protocol.type_OKSingleApp or
              type_f == Type_protocol.type_OKDSingleApp or type_f == Type_protocol.type_OKOUSingleApp):
            pass
            parserOK2(doc, path_xml, filexml, reg, type_f)
        elif type_f == Type_protocol.type_ZPFinal:
            pass
            parserZPFinal(doc, path_xml, filexml, reg, type_f)
        elif type_f == Type_protocol.type_OK1 or type_f == Type_protocol.type_OKD1 or type_f == Type_protocol.type_OKD2 or \
                type_f == Type_protocol.type_OKD3 or type_f == Type_protocol.type_OKD4 or \
                type_f == Type_protocol.type_OKOU1 or type_f == Type_protocol.type_OKOU2:
            pass
            parserOK1(doc, path_xml, filexml, reg, type_f)
        elif type_f == Type_protocol.type_Cancel:
            pass
            parserCancel(doc, path_xml, filexml, reg, type_f)
        else:
            parserOther(doc, path_xml, filexml, reg, type_f)
    except Exception as e:
        logging_parser("Ошибка в функции parser", e, path_xml, type_f)
        traceback.print_tb(e.__traceback__)
        pass
