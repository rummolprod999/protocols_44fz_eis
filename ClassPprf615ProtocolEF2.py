import datetime

import dateutil.parser
import json
import pytz
import itertools

import UtilsFunctions
from ClassParticipiant504 import Participiant504
from ClassProtocol504 import Protocol504
from connect_to_db import connect_bd
from VarExecut import PREFIX, DB
from UtilsFunctions import logging_parser


class Pprf615ProtocolEF2(Protocol504, Participiant504):
    add = 0
    update = 0

    def get_app_rating(self, application):
        d = UtilsFunctions.get_el(application, 'commonInfo', 'appRating')
        if not d:
            d = 0
        return d

    def get_admission(self, application):
        d = ''
        appRejectedReason = UtilsFunctions.get_el(application, 'admittedInfo', 'appNotAdmittedInfo',
                                                  'appRejectedReasonsInfo',
                                                  'appRejectedReasonInfo')
        if appRejectedReason:
            reasons = UtilsFunctions.generator_univ(appRejectedReason)
            if UtilsFunctions.check_yeld(reasons):
                for r in list(UtilsFunctions.generator_univ(appRejectedReason)):
                    d += f"{UtilsFunctions.get_el(r, 'rejectReason', 'name')} ".strip()
        else:
            d = UtilsFunctions.get_el(application, 'admittedInfo',
                                      'admitted') or UtilsFunctions.get_el(application, 'admittedInfo',
                                                                           'appAdmittedInfo', 'admitted')
            if d == 'true':
                d = 'Допущен'
            elif d == 'false':
                d = 'Не допущен'
            if not d:
                d = UtilsFunctions.get_el(application, 'notConsidered')
                if d == 'true':
                    d = 'Заявка не рассматривалась'
        return d

    def get_price(self, application):
        d = UtilsFunctions.get_el(application, 'finalPrice')
        if not d:
            d = UtilsFunctions.get_el(application, 'lastPriceOffer', 'price')
        return d

    def get_abandoned_reason(self):
        d = UtilsFunctions.get_el(self.protocol, 'protocolInfo', 'abandonedReason', 'name')
        k = UtilsFunctions.get_el(self.protocol, 'protocolInfo', 'abandonedReason', 'code')
        if d and k:
            return f'{d}|{k}'
        return d or k

    def get_protocol_date(self):
        d = UtilsFunctions.get_el(self.protocol, 'commonInfo', 'docPublishDate')
        if d:
            try:
                dt = dateutil.parser.parse(d)
                d = dt.astimezone(pytz.timezone("Europe/Moscow"))
            except Exception:
                d = ''
        else:
            d = ''
        return str(d)

    def get_applications(self):
        d = UtilsFunctions.generator_univ(
                UtilsFunctions.get_el_list(self.protocol, 'protocolInfo', 'applications', 'application'))
        return d

    def get_journal_number(self, application):
        d = UtilsFunctions.get_el(application, 'journalNumber')
        return d


def parserPprf615ProtocolEF2(doc, path_xml, filexml, reg, type_f):
    type_f = "pprf615ProtocolEF2"
    p = Pprf615ProtocolEF2(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url_external()
    print_form = p.get_print_form_ext()
    protocol_date = p.get_protocol_date()
    lot_number = 1
    abandoned_reason_name = p.get_abandoned_reason()
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
    dop_info = p.get_dop_info(p)
    cur.execute(
            f"""INSERT INTO {PREFIX}auction_end_protocol SET id_protocol = %s, protocol_date =  %s, purchase_number = %s, 
                            url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, lot_number = %s,  abandoned_reason_name = %s, dop_info = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status, lot_number,
             abandoned_reason_name, dop_info))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        Pprf615ProtocolEF2.update += 1
    else:
        Pprf615ProtocolEF2.add += 1
    applications = p.get_applications()
    for app in applications:
        id_participiant = 0
        journal_number = p.get_journal_number(app)
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_fact_address(app)
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
            # logging_parser('Нет инн', xml, type_f)
            pass
        app_rating = p.get_app_rating(app)
        admission = p.get_admission(app)
        price = p.get_price(app)
        cur.execute(f"""INSERT INTO {PREFIX}auction_end_applications SET id_auction_end_protocol = %s, 
                                journal_number = %s, app_rating = %s, admission = %s, 
                                id_participiant = %s, price = %s""",
                    (id_p, journal_number, app_rating,
                     admission, id_participiant, price))
    p.add_attach(cur, id_p)
    cur.close()
    con.close()
