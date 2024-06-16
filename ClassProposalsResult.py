import datetime

import dateutil.parser
import pytz
import json

import UtilsFunctions
from ClassParticipiant import Participiant
from ClassProtocol import Protocol
from connect_to_db import connect_bd
from VarExecut import PREFIX, DB
from UtilsFunctions import logging_parser


class ProtocolProposalsResult(Protocol, Participiant):
    add = 0
    update = 0

    def get_id(self):
        d = UtilsFunctions.get_el(self.protocol, 'registryNum')
        return d

    def get_url(self):
        d = UtilsFunctions.get_el(self.protocol, 'printForm', 'url')
        return d

    def get_app_rating(self, application):
        d = UtilsFunctions.get_el(application, 'appRating')
        if not d:
            d = 0
        return d

    def get_abandoned_reason_name(self):
        try:
            d = UtilsFunctions.get_el_list(self.protocol, 'attachments', 'attachment')
            return UtilsFunctions.get_el(d[0], 'docDescription') if len(d) > 0 else ''
        except:
            return UtilsFunctions.get_el(self.protocol, 'attachments', 'attachment', 'docDescription')

    def get_protocol_date(self):
        d = UtilsFunctions.get_el(self.protocol, 'createDate')
        if d:
            try:
                dt = dateutil.parser.parse(d)
                d = dt.astimezone(pytz.timezone("Europe/Moscow"))
            except Exception:
                d = ''
        else:
            d = ''
        return str(d)

    def get_dop_info(self, p):
        dop_info = p.protocol
        try:
            del dop_info['extPrintFormInfo']['signature']
        except:
            pass
        try:
            del dop_info['attachments']['attachment']['cryptoSigns']
        except:
            try:
                for e in dop_info['attachments']['attachment']:
                    del e['cryptoSigns']
            except:
                pass
        try:
            del dop_info['extPrintFormInfo']['commissionSignatures']
        except:
            pass
        try:
            del dop_info['attachmentsInfo']['attachmentInfo']['cryptoSigns']
        except:
            try:
                for e in dop_info['attachmentsInfo']['attachmentInfo']:
                    del e['cryptoSigns']
            except:
                pass
        dop_info = json.dumps(dop_info, sort_keys=False,
                              indent=4,
                              ensure_ascii=False,
                              separators=(',', ': '))
        return dop_info


def parserProposalsResult(doc, path_xml, filexml, reg, type_f):
    p = ProtocolProposalsResult(doc, filexml)
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
        ProtocolProposalsResult.update += 1
    else:
        ProtocolProposalsResult.add += 1
    for app in p.applications:
        id_participiant = 0
        journal_number = p.get_journal_number(app)
        inn = p.get_inn(app)
        kpp = p.get_kpp(app)
        organization_name = p.get_organization_name(app)
        participant_type = p.get_participant_type(app)
        country_full_name = p.get_country_full_name(app)
        post_address = p.get_post_address(app)
        if organization_name:
            cur.execute(f"""SELECT id FROM {PREFIX}auction_participant WHERE organization_name = %s""",
                        (organization_name))
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
            logging_parser('Нет fullName', xml, type_f)
        app_rating = p.get_app_rating(app)
        admission = ''
        price = ''
        cur.execute(f"""INSERT INTO {PREFIX}auction_end_applications SET id_auction_end_protocol = %s, 
                                journal_number = %s, app_rating = %s, admission = %s, 
                                id_participiant = %s, price = %s""",
                    (id_p, journal_number, app_rating,
                     admission, id_participiant, price))
    cur.close()
    con.close()
