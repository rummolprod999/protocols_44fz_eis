import datetime

import dateutil.parser

import UtilsFunctions
from ClassProtocolEOK2 import ProtocolEOK2
from UtilsFunctions import logging_parser
from VarExecut import PREFIX, DB
from connect_to_db import connect_bd


class ProtocolEOK1(ProtocolEOK2):
    add_protocolEOK1 = 0
    update_protocolEOK1 = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)

    def get_abandoned_reason(self):
        d = UtilsFunctions.get_el(self.protocol, 'abandonedReason', 'name')
        k = UtilsFunctions.get_el(self.protocol, 'abandonedReason', 'code')
        if d and k:
            return f'{d}|{k}'
        return d or k

    def get_price(self, application):
        d = UtilsFunctions.get_el(application, 'admittedInfo', 'singleAppAdmittedInfo', 'price')
        return d


def parserEOK1(doc, path_xml, filexml, reg, type_f):
    p = ProtocolEOK1(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    # print(purchase_number)
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url_external()
    print_form = p.get_print_form_ext()
    protocol_date = p.get_protocol_date()
    con = connect_bd(DB)
    cur = con.cursor()
    lot_number = 1
    abandoned_reason_name = p.get_abandoned_reason()
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
        ProtocolEOK1.update_protocolEOK1 += 1
    else:
        ProtocolEOK1.add_protocolEOK1 += 1
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
        price = p.get_price(app)
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
                                                    id_participiant = %s, price = %s""",
                    (id_p, journal_number, app_rating, admission, id_participiant, price))
    p.add_attach(cur, id_p)
    cur.close()
    con.close()
