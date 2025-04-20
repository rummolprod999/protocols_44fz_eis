import datetime

import dateutil.parser
import pytz

import UtilsFunctions
from ClassProtocol import Protocol
from UtilsFunctions import logging_parser
from VarExecut import PREFIX, DB
from connect_to_db import connect_bd


class ProtocolCancel(Protocol):
    add_protocolCancel = 0
    update_protocolCancel = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)

    def get_protocol_number(self):
        d = UtilsFunctions.get_el(self.protocol, 'protocolNumber')
        return d

    def get_protocol_date(self):
        d = UtilsFunctions.get_el(self.protocol, 'docPublishDate')
        if d:
            try:
                dt = dateutil.parser.parse(d)
                d = dt.astimezone(pytz.timezone("Europe/Moscow"))
            except Exception:
                d = ''
        else:
            d = ''
        return str(d)

    def get_authority_name(self):
        d = UtilsFunctions.get_el(self.protocol, 'cancelReason', 'authorityPrescription', 'externalPrescription',
                                  'authorityName') or UtilsFunctions.get_el(self.protocol, 'cancelReason',
                                                                            'authorityPrescription',
                                                                            'reestrPrescription',
                                                                            'authorityName') or UtilsFunctions.get_el(
                self.protocol, 'cancelReason',
                'courtDecision', 'courtName')
        return d

    def get_doc_name(self):
        d = UtilsFunctions.get_el(self.protocol, 'cancelReason', 'authorityPrescription', 'externalPrescription',
                                  'docName') or UtilsFunctions.get_el(self.protocol, 'cancelReason',
                                                                      'authorityPrescription', 'reestrPrescription',
                                                                      'docName') or UtilsFunctions.get_el(
                self.protocol, 'cancelReason',
                'courtDecision', 'docName')
        return d


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
