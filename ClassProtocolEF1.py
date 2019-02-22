import datetime

import dateutil.parser

import UtilsFunctions
from ClassProtocol import Protocol
from connect_to_db import connect_bd
from VarExecut import PREFIX, DB
from UtilsFunctions import logging_parser


class ProtocolEF1(Protocol):
    add_protocolEF1 = 0
    update_protocolEF1 = 0

    def get_abandoned_reason_name(self):
        d = UtilsFunctions.get_el(self.protocol, 'protocolLot', 'abandonedReason', 'name')
        return d

    def get_admission(self, application):
        d = UtilsFunctions.get_el(application, 'admitted')
        if d == 'true':
            d = 'Допущен'
        if not d:
            d = UtilsFunctions.get_el(application, 'notConsidered')
            if d == 'true':
                d = 'Заявка не рассматривалась'
        if not d:
            appRejectedReason = UtilsFunctions.get_el(application, 'appRejectedReason')
            if appRejectedReason:
                reasons = UtilsFunctions.generator_univ(appRejectedReason)
                if UtilsFunctions.check_yeld(reasons):
                    for r in list(UtilsFunctions.generator_univ(appRejectedReason)):
                        d += "{0} ".format(UtilsFunctions.get_el(r, 'explanation'))
        return d


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
