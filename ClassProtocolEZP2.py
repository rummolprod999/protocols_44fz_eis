import datetime

import dateutil.parser

import UtilsFunctions
import parser_prot
from ClassParticipiant504 import Participiant504
from ClassProtocol504 import Protocol504
from connect_to_db import connect_bd
from parser_prot import DB, PREFIX
from UtilsFunctions import logging_parser


class ProtocolEZP2(Protocol504, Participiant504):
    add_protocolEZP2 = 0
    update_protocolEZP2 = 0

    def get_app_rating(self, application):
        d = UtilsFunctions.get_el(application, 'admittedInfo', 'appAdmittedInfo', 'appRating')
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
        return d

    def get_price(self, application):
        d = UtilsFunctions.get_el(application, 'admittedInfo', 'appAdmittedInfo', 'price')
        return d

    def get_abandoned_reason_name(self):
        d = UtilsFunctions.get_el(self.protocol, 'protocolInfo', 'abandonedReason', 'name')
        return d


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
