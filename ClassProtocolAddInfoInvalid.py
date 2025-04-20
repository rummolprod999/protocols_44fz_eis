import datetime

import dateutil.parser
import pytz

import UtilsFunctions
from ClassAddInfo import ProtocolAddInfo
from UtilsFunctions import logging_parser
from VarExecut import PREFIX, DB
from connect_to_db import connect_bd


class ProtocolAddInfoInvalid(ProtocolAddInfo):
    add = 0
    update = 0

    def get_protocol_date(self):
        d = UtilsFunctions.get_el(self.protocol, 'invalidityInfo', 'date')
        if not d:
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

    def get_abandoned_reason_name(self):
        v = ''
        try:
            d = UtilsFunctions.get_el_list(self.protocol, 'attachments', 'attachment')
            v = UtilsFunctions.get_el(d[0], 'docDescription') if len(d) > 0 else ''
        except:
            v = UtilsFunctions.get_el_list(self.protocol, 'attachments', 'attachment', 'docDescription')
        t = UtilsFunctions.get_el(self.protocol, 'invalidityInfo', 'reason')

        return t + ' | ' + v


def parserAddInfoInvalid(doc, path_xml, filexml, reg, type_f):
    p = ProtocolAddInfoInvalid(doc, filexml)
    purchase_number = p.get_purchaseNumber()
    if not purchase_number:
        logging_parser('У протокола нет purchase_number', path_xml)
        return
    xml = path_xml[path_xml.find('/') + 1:][(path_xml[path_xml.find('/') + 1:]).find('/') + 1:]
    id_protocol = p.get_id()
    url = p.get_url()
    print_form = p.get_print_form_ext()
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
    ref_fact = ''
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
                    url = %s, print_form = %s, xml = %s, type_protocol = %s, cancel = %s, abandoned_reason_name = %s, lot_number = %s, refusal_fact = %s, dop_info = %s""",
            (id_protocol, protocol_date, purchase_number, url, print_form, xml, type_f, cancel_status,
             abandoned_reason_name, lot_number, ref_fact, dop_info))
    id_p = cur.lastrowid
    if not id_p:
        logging_parser('Не получили id', xml)
    if updated:
        ProtocolAddInfoInvalid.update += 1
    else:
        ProtocolAddInfoInvalid.add += 1
    cur.close()
    con.close()
