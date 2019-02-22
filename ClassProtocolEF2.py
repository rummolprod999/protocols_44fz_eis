import datetime

import dateutil.parser

import UtilsFunctions
from ClassProtocol import Protocol
from connect_to_db import connect_bd
from VarExecut import PREFIX, DB
from UtilsFunctions import logging_parser


class ProtocolEF2(Protocol):
    add_protocolEF2 = 0
    update_protocolEF2 = 0

    def get_offer_first_price(self, application):
        d = UtilsFunctions.get_el(application, 'priceOffers', 'firstOffer', 'price')
        if not d:
            d = 0.0
        return d

    def get_offer_last_price(self, application):
        d = UtilsFunctions.get_el(application, 'priceOffers', 'lastOffer', 'price')
        if not d:
            d = 0.0
        return d

    def get_offer_quantity(self, application):
        d = UtilsFunctions.get_el(application, 'priceOffers', 'offersQuantity')
        if not d:
            d = 0
        return d


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
