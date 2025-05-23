import datetime

import dateutil.parser

from ClassProtocolOK2 import ProtocolOK2
from UtilsFunctions import logging_parser
from VarExecut import PREFIX, DB
from connect_to_db import connect_bd


class ProtocolOK1(ProtocolOK2):
    add_protocolOK1 = 0
    update_protocolOK1 = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)


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
