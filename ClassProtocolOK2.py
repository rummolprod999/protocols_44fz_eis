import datetime
import itertools

import dateutil.parser

import parser_prot
from ClassParticipiant import Participiant
from ClassProtocol import Protocol
from connect_to_db import connect_bd
from parser_prot import logging_parser, DB, PREFIX


class ProtocolOK2(Protocol, Participiant):
    add_protocolOK2 = 0
    update_protocolOK2 = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)
        self.lots = parser_prot.generator_univ(parser_prot.get_el_list(self.protocol, 'protocolLots', 'protocolLot'))

    def get_lot_number(self, lot):
        d = parser_prot.get_el(lot, 'lotNumber')
        return d

    def get_applications(self, lot):
        d = parser_prot.generator_univ(parser_prot.get_el_list(lot, 'applications', 'application'))
        p, d = itertools.tee(d)
        if not parser_prot.check_yeld(p):
            d = parser_prot.generator_univ(parser_prot.get_el_list(lot, 'application'))
        return d

    def get_participiants(self, application):
        d = parser_prot.generator_univ(parser_prot.get_el_list(application, 'appParticipants', 'appParticipant'))
        return d

    def get_app_rating(self, application):
        d = parser_prot.get_el(application, 'admittedInfo', 'appRating')
        if not d:
            d = 0
        return d

    def get_inn(self, part):
        d = parser_prot.get_el(part, 'inn') or parser_prot.get_el(part, 'idNumber')
        return d

    def get_kpp(self, part):
        d = parser_prot.get_el(part, 'kpp')
        return d

    def get_organization_name(self, part):
        d = parser_prot.get_el(part, 'organizationName')
        if not d:
            lastName = parser_prot.get_el(part, 'contactInfo',
                                          'lastName')
            firstName = parser_prot.get_el(part, 'contactInfo',
                                           'firstName')
            middleName = parser_prot.get_el(part, 'contactInfo',
                                            'middleName')
            d = f"{lastName} {firstName} {middleName}".strip()
        return d

    def get_participant_type(self, part):
        d = parser_prot.get_el(part, 'participantType')
        return d

    def get_country_full_name(self, part):
        d = parser_prot.get_el(part, 'country', 'countryFullName')
        return d

    def get_post_address(self, part):
        d = parser_prot.get_el(part, 'postAddress')
        return d

    def get_abandoned_reason_name(self, lot):
        d = parser_prot.get_el(lot, 'abandonedReason', 'name')
        return d

    def get_admission(self, application):
        d = ''
        appRejectedReason = parser_prot.get_el(application, 'admittedInfo', 'appRejectedReason')
        if appRejectedReason:
            reasons = parser_prot.generator_univ(appRejectedReason)
            if parser_prot.check_yeld(reasons):
                for r in list(parser_prot.generator_univ(appRejectedReason)):
                    d += "{0} ".format(parser_prot.get_el(r, 'nsiRejectReason', 'reason'))
        return d


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
