import itertools
import dateutil.parser
import pytz
import parser_prot


class Participiant504:
    def get_inn(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'inn') or parser_prot.get_el(application,
                                                                                           'appParticipant',
                                                                                           'idNumber') or parser_prot.get_el(
                application, 'appParticipants', 'appParticipant', 'idNumber') or parser_prot.get_el(application,
                                                                                                    'appParticipants',
                                                                                                    'appParticipant',
                                                                                                    'inn') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'INN') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'INN')
        return d

    def get_kpp(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'kpp') or parser_prot.get_el(application,
                                                                                           'appParticipants',
                                                                                           'appParticipant',
                                                                                           'kpp') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'KPP')
        return d

    def get_organization_name(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'organizationName') or parser_prot.get_el(application,
                                                                                                        'appParticipants',
                                                                                                        'appParticipant',
                                                                                                        'organizationName') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'fullName') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'fullName')
        if not d:
            lastName = parser_prot.get_el(application, 'appParticipant', 'contactInfo',
                                          'lastName') or parser_prot.get_el(application, 'appParticipants',
                                                                            'appParticipant', 'contactInfo',
                                                                            'lastName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'legalEntityRFInfo', 'contactInfo', 'lastName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'lastName')
            firstName = parser_prot.get_el(application, 'appParticipant', 'contactInfo',
                                           'firstName') or parser_prot.get_el(application, 'appParticipants',
                                                                              'appParticipant', 'contactInfo',
                                                                              'firstName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'legalEntityRFInfo', 'contactInfo', 'firstName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'firstName')
            middleName = parser_prot.get_el(application, 'appParticipant', 'contactInfo',
                                            'middleName') or parser_prot.get_el(application, 'appParticipants',
                                                                                'appParticipant', 'contactInfo',
                                                                                'middleName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'legalEntityRFInfo', 'contactInfo', 'middleName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'middleName')
            d = f"{lastName} {firstName} {middleName}".strip()
        return d

    def get_participant_type(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'participantType') or parser_prot.get_el(application,
                                                                                                       'appParticipants',
                                                                                                       'appParticipant',
                                                                                                       'participantType') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'participantType')
        return d

    def get_country_full_name(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'country', 'countryFullName') or parser_prot.get_el(
                application,
                'appParticipants',
                'appParticipant', 'country',
                'countryFullName') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo', 'country',
                'countryFullName')
        return d

    def get_post_address(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'postAddress') or parser_prot.get_el(application,
                                                                                                   'appParticipants',
                                                                                                   'appParticipant',
                                                                                                   'postAddress') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'contactInfo', 'orgPostAddress') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'postAddress')
        return d


class Participiant:
    def get_inn(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'inn') or parser_prot.get_el(application,
                                                                                           'appParticipant',
                                                                                           'idNumber') or parser_prot.get_el(
                application, 'appParticipants', 'appParticipant', 'idNumber') or parser_prot.get_el(application,
                                                                                                    'appParticipants',
                                                                                                    'appParticipant',
                                                                                                    'inn') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'INN') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'INN')
        return d

    def get_kpp(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'kpp') or parser_prot.get_el(application,
                                                                                           'appParticipants',
                                                                                           'appParticipant',
                                                                                           'kpp') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'KPP') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'KPP') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'KPP')
        return d

    def get_organization_name(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'organizationName') or parser_prot.get_el(application,
                                                                                                        'appParticipants',
                                                                                                        'appParticipant',
                                                                                                        'organizationName') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'legalEntityRFInfo',
                'fullName')
        if not d:
            lastName = parser_prot.get_el(application, 'appParticipant', 'contactInfo',
                                          'lastName') or parser_prot.get_el(application, 'appParticipants',
                                                                            'appParticipant', 'contactInfo',
                                                                            'lastName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'lastName')
            firstName = parser_prot.get_el(application, 'appParticipant', 'contactInfo',
                                           'firstName') or parser_prot.get_el(application, 'appParticipants',
                                                                              'appParticipant', 'contactInfo',
                                                                              'firstName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'firstName')
            middleName = parser_prot.get_el(application, 'appParticipant', 'contactInfo',
                                            'middleName') or parser_prot.get_el(application, 'appParticipants',
                                                                                'appParticipant', 'contactInfo',
                                                                                'middleName') or parser_prot.get_el(
                    application, 'appParticipantInfo',
                    'individualPersonRFInfo', 'nameInfo', 'middleName')
            d = f"{lastName} {firstName} {middleName}".strip()
        return d

    def get_participant_type(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'participantType') or parser_prot.get_el(application,
                                                                                                       'appParticipants',
                                                                                                       'appParticipant',
                                                                                                       'participantType')
        return d

    def get_country_full_name(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'country', 'countryFullName') or parser_prot.get_el(
                application,
                'appParticipants',
                'appParticipant', 'country',
                'countryFullName')
        return d

    def get_post_address(self, application):
        d = parser_prot.get_el(application, 'appParticipant', 'postAddress') or parser_prot.get_el(application,
                                                                                                   'appParticipants',
                                                                                                   'appParticipant',
                                                                                                   'postAddress') or parser_prot.get_el(
                application,
                'appParticipantInfo',
                'individualPersonRFInfo',
                'postAddress')
        return d
        return d


class Protocol:
    def __init__(self, protocol, xml):
        prot = protocol[list(protocol.keys())[0]]
        list_p = [v for v in prot.keys() if 'fcs' in v.lower()]
        self.protocol = prot[list_p[0]]
        self.xml = xml
        if 'protocolLot' in self.protocol:
            if self.protocol['protocolLot'] is None:
                self.applications = []
            elif 'applications' in self.protocol['protocolLot']:
                if 'application' in self.protocol['protocolLot']['applications']:
                    self.applications = parser_prot.generator_univ(
                            self.protocol['protocolLot']['applications']['application'])
                else:
                    self.applications = []
            elif 'application' in self.protocol['protocolLot']:
                self.applications = parser_prot.generator_univ(self.protocol['protocolLot']['application'])
            else:
                self.applications = []
        else:
            self.applications = []

    def get_purchaseNumber(self):
        d = parser_prot.get_el(self.protocol, 'purchaseNumber')
        return d

    def get_id(self):
        d = parser_prot.get_el(self.protocol, 'id')
        return d

    def get_protocol_date(self):
        d = parser_prot.get_el(self.protocol, 'protocolDate')
        if d:
            try:
                dt = dateutil.parser.parse(d)
                d = dt.astimezone(pytz.timezone("Europe/Moscow"))
            except Exception:
                d = ''
        else:
            d = ''
        return str(d)

    def get_url(self):
        d = parser_prot.get_el(self.protocol, 'href')
        return d

    def get_print_form(self):
        d = parser_prot.get_el(self.protocol, 'printForm', 'url')
        if d.startswith("<![CDATA"):
            d = d[9:-3]
        return d

    def get_journal_number(self, application):
        d = parser_prot.get_el(application, 'journalNumber')
        return d


class ProtocolEF2(Protocol):
    add_protocolEF2 = 0
    update_protocolEF2 = 0

    def get_offer_first_price(self, application):
        d = parser_prot.get_el(application, 'priceOffers', 'firstOffer', 'price')
        if not d:
            d = 0.0
        return d

    def get_offer_last_price(self, application):
        d = parser_prot.get_el(application, 'priceOffers', 'lastOffer', 'price')
        if not d:
            d = 0.0
        return d

    def get_offer_quantity(self, application):
        d = parser_prot.get_el(application, 'priceOffers', 'offersQuantity')
        if not d:
            d = 0
        return d


class ProtocolEF1(Protocol):
    add_protocolEF1 = 0
    update_protocolEF1 = 0

    def get_abandoned_reason_name(self):
        d = parser_prot.get_el(self.protocol, 'protocolLot', 'abandonedReason', 'name')
        return d

    def get_admission(self, application):
        d = parser_prot.get_el(application, 'admitted')
        if d == 'true':
            d = 'Допущен'
        if not d:
            d = parser_prot.get_el(application, 'notConsidered')
            if d == 'true':
                d = 'Заявка не рассматривалась'
        if not d:
            appRejectedReason = parser_prot.get_el(application, 'appRejectedReason')
            if appRejectedReason:
                reasons = parser_prot.generator_univ(appRejectedReason)
                if parser_prot.check_yeld(reasons):
                    for r in list(parser_prot.generator_univ(appRejectedReason)):
                        d += "{0} ".format(parser_prot.get_el(r, 'explanation'))
        return d


class ProtocolEF3(Protocol, Participiant):
    add_protocolEF3 = 0
    update_protocolEF3 = 0

    def get_app_rating(self, application):
        d = parser_prot.get_el(application, 'appRating')
        if not d:
            d = 0
        return d

    def get_abandoned_reason_name(self):
        d = parser_prot.get_el(self.protocol, 'protocolLot', 'abandonedReason', 'name')
        return d

    def get_admission(self, application):
        d = parser_prot.get_el(application, 'admitted')
        if d == 'true':
            d = 'Допущен'
        if not d:
            d = parser_prot.get_el(application, 'notConsidered')
            if d == 'true':
                d = 'Заявка не рассматривалась'
        if not d:
            appRejectedReason = parser_prot.get_el(application, 'appRejectedReason')
            if appRejectedReason:
                reasons = parser_prot.generator_univ(appRejectedReason)
                if parser_prot.check_yeld(reasons):
                    for r in list(parser_prot.generator_univ(appRejectedReason)):
                        d += "{0} ".format(parser_prot.get_el(r, 'nsiRejectReason', 'reason'))
        return d

    def get_refusalFact_name(self):
        d = parser_prot.get_el(self.protocol, 'refusalFact', 'foundation', 'name')
        return d

    def get_ref_explation(self):
        d = parser_prot.get_el(self.protocol, 'refusalFact', 'explanation')
        return d


class ProtocolZPFinal(ProtocolEF3):
    add_protocolZPFinal = 0
    update_protocolZPFinal = 0

    def get_price(self, application):
        d = parser_prot.get_el(application, 'lastOffer', 'price')
        return d


class ProtocolZK(Protocol, Participiant):
    add_protocolZK = 0
    update_protocolZK = 0

    def get_abandoned_reason_name(self):
        d = parser_prot.get_el(self.protocol, 'protocolLot', 'abandonedReason', 'name')
        return d

    def test_abandoned_reason_name(self):
        d = parser_prot.get_el(self.protocol, 'protocolLot', 'abandonedReason')
        if type(d) == list:
            parser_prot.logging_parser('множество abandoned_reason', self.xml)

    def get_lot_number(self):
        d = parser_prot.get_el(self.protocol, 'protocolLot', 'lotNumber')
        if not d:
            d = 1
        return d

    def get_result_zk(self, application):
        d = parser_prot.get_el(application, 'admittedInfo', 'resultType')
        return d

    def get_price(self, application):
        d = parser_prot.get_el(application, 'price')
        return d


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


class ProtocolOK1(ProtocolOK2):
    add_protocolOK1 = 0
    update_protocolOK1 = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)


class ProtocolCancel(Protocol):
    add_protocolCancel = 0
    update_protocolCancel = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)

    def get_protocol_number(self):
        d = parser_prot.get_el(self.protocol, 'protocolNumber')
        return d

    def get_protocol_date(self):
        d = parser_prot.get_el(self.protocol, 'docPublishDate')
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
        d = parser_prot.get_el(self.protocol, 'cancelReason', 'authorityPrescription', 'externalPrescription',
                               'authorityName') or parser_prot.get_el(self.protocol, 'cancelReason',
                                                                      'authorityPrescription', 'reestrPrescription',
                                                                      'authorityName') or parser_prot.get_el(
                self.protocol, 'cancelReason',
                'courtDecision', 'courtName')
        return d

    def get_doc_name(self):
        d = parser_prot.get_el(self.protocol, 'cancelReason', 'authorityPrescription', 'externalPrescription',
                               'docName') or parser_prot.get_el(self.protocol, 'cancelReason',
                                                                'authorityPrescription', 'reestrPrescription',
                                                                'docName') or parser_prot.get_el(
                self.protocol, 'cancelReason',
                'courtDecision', 'docName')
        return d


class Protocol504:
    def __init__(self, protocol, xml):
        prot = protocol[list(protocol.keys())[0]]
        list_p = [v for v in prot.keys() if v.lower().startswith("ep")]
        self.protocol = prot[list_p[0]]
        self.xml = xml
        if 'protocolInfo' in self.protocol:
            if self.protocol['protocolInfo'] is None:
                self.applications = []
            elif 'applicationsInfo' in self.protocol['protocolInfo']:
                if 'applicationInfo' in self.protocol['protocolInfo']['applicationsInfo']:
                    self.applications = parser_prot.generator_univ(
                            self.protocol['protocolInfo']['applicationsInfo']['applicationInfo'])
                else:
                    self.applications = []
            elif 'applicationInfo' in self.protocol['protocolInfo']:
                self.applications = parser_prot.generator_univ(self.protocol['protocolInfo']['applicationInfo'])
            else:
                self.applications = []
        else:
            self.applications = []

    def get_purchaseNumber(self):
        d = parser_prot.get_el(self.protocol, 'commonInfo', 'purchaseNumber')
        return d

    def get_id(self):
        d = parser_prot.get_el(self.protocol, 'id')
        return d

    def get_protocol_date(self):
        d = parser_prot.get_el(self.protocol, 'commonInfo', 'publishDTInEIS')
        if d:
            try:
                dt = dateutil.parser.parse(d)
                d = dt.astimezone(pytz.timezone("Europe/Moscow"))
            except Exception:
                d = ''
        else:
            d = ''
        return str(d)

    def get_url(self):
        d = parser_prot.get_el(self.protocol, 'commonInfo', 'href')
        return d

    def get_print_form(self):
        d = parser_prot.get_el(self.protocol, 'printFormInfo', 'url')
        if d.startswith("<![CDATA"):
            d = d[9:-3]
        return d

    def get_journal_number(self, application):
        d = parser_prot.get_el(application, 'commonInfo', 'appNumber')
        return d


class ProtocolEOK2(Protocol504, Participiant504):
    add_protocolEOK2 = 0
    update_protocolEOK2 = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)

    def get_participiants(self, application):
        d = parser_prot.generator_univ(parser_prot.get_el_list(application, 'appParticipants', 'appParticipant'))
        return d

    def get_app_rating(self, application):
        d = parser_prot.get_el(application, 'admittedInfo', 'appRating')
        if not d:
            d = 0
        return d

    def get_abandoned_reason_name(self):
        d = parser_prot.get_el(self.protocol, 'protocolInfo', 'abandonedReason', 'name')
        return d

    def get_admission(self, application):
        d = ''
        appRejectedReason = parser_prot.get_el(application, 'admittedInfo', 'appNotAdmittedInfo',
                                               'appRejectedReasonsInfo',
                                               'appRejectedReasonInfo')
        if appRejectedReason:
            reasons = parser_prot.generator_univ(appRejectedReason)
            if parser_prot.check_yeld(reasons):
                for r in list(parser_prot.generator_univ(appRejectedReason)):
                    d += f"{parser_prot.get_el(r, 'rejectReason', 'name')} ".strip()
        return d


class ProtocolEOK1(ProtocolEOK2):
    add_protocolEOK1 = 0
    update_protocolEOK1 = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)


class ProtocolEZP1(ProtocolEOK2):
    add_protocolEZP1 = 0
    update_protocolEZP1 = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)


class ProtocolEZK2(Protocol504, Participiant504):
    add_protocolEZK2 = 0
    update_protocolEZK2 = 0

    def get_abandoned_reason_name(self):
        d = parser_prot.get_el(self.protocol, 'protocolInfo', 'abandonedReason', 'name')
        return d

    def test_abandoned_reason_name(self):
        d = parser_prot.get_el(self.protocol, 'protocolInfo', 'abandonedReason')
        if type(d) == list:
            parser_prot.logging_parser('множество abandoned_reason', self.xml)

    def get_lot_number(self):
        d = parser_prot.get_el(self.protocol, 'protocolInfo', 'lotNumber')
        if not d:
            d = 1
        return d

    def get_result_zk(self, application):
        d = parser_prot.get_el(application, 'admittedInfo', 'appAdmittedInfo', 'resultType')
        return d

    def get_price(self, application):
        d = parser_prot.get_el(application, 'finalPrice')
        return d

    def get_admission(self, application):
        d = ''
        appRejectedReason = parser_prot.get_el(application, 'admittedInfo', 'appNotAdmittedInfo',
                                               'appRejectedReasonsInfo',
                                               'appRejectedReasonInfo')
        if appRejectedReason:
            reasons = parser_prot.generator_univ(appRejectedReason)
            if parser_prot.check_yeld(reasons):
                for r in list(parser_prot.generator_univ(appRejectedReason)):
                    d += f"{parser_prot.get_el(r, 'rejectReason', 'name')} ".strip()
        return d


class ProtocolEZP2(Protocol504, Participiant504):
    add_protocolEZP2 = 0
    update_protocolEZP2 = 0

    def get_app_rating(self, application):
        d = parser_prot.get_el(application, 'admittedInfo', 'appAdmittedInfo', 'appRating')
        if not d:
            d = 0
        return d

    def get_admission(self, application):
        d = ''
        appRejectedReason = parser_prot.get_el(application, 'admittedInfo', 'appNotAdmittedInfo',
                                               'appRejectedReasonsInfo',
                                               'appRejectedReasonInfo')
        if appRejectedReason:
            reasons = parser_prot.generator_univ(appRejectedReason)
            if parser_prot.check_yeld(reasons):
                for r in list(parser_prot.generator_univ(appRejectedReason)):
                    d += f"{parser_prot.get_el(r, 'rejectReason', 'name')} ".strip()
        return d

    def get_price(self, application):
        d = parser_prot.get_el(application, 'admittedInfo', 'appAdmittedInfo', 'price')
        return d

    def get_abandoned_reason_name(self):
        d = parser_prot.get_el(self.protocol, 'protocolInfo', 'abandonedReason', 'name')
        return d


class Type_protocol:
    type_EF1 = 'ProtocolEF1'
    type_EF2 = 'ProtocolEF2'
    type_EF3 = 'ProtocolEF3'
    type_ZK = 'ProtocolZK'
    type_ZKAfterProlong = 'ZKAfterProlong'
    type_EFSingleApp = 'ProtocolEFSingleApp'
    type_EFSinglePart = 'ProtocolEFSinglePart'
    type_OK2 = 'ProtocolOK2'
    type_OKD5 = 'ProtocolOKD5'
    type_OKOU3 = 'ProtocolOKOU3'
    type_ZPFinal = 'ProtocolZPFinal'
    type_Deviation = 'ProtocolDeviation'
    type_EFInvalidation = 'ProtocolEFInvalidation'
    type_OKSingleApp = 'ProtocolOKSingleApp'
    type_OKDSingleApp = 'ProtocolOKDSingleApp'
    type_OKOUSingleApp = 'ProtocolOKOUSingleApp'
    type_OK1 = 'ProtocolOK1'
    type_OKD1 = 'ProtocolOKD1'
    type_OKD2 = 'ProtocolOKD2'
    type_OKD3 = 'ProtocolOKD3'
    type_OKD4 = 'ProtocolOKD4'
    type_OKOU1 = 'ProtocolOKOU1'
    type_OKOU2 = 'ProtocolOKOU2'
    type_Cancel = 'ProtocolCancel'


class Type_protocol504:
    type_EOK1 = 'epProtocolEOK1'
    type_EOK2 = 'epProtocolEOK2'
    type_EOK3 = 'epProtocolEOK3'
    type_EOKSingleApp = 'epProtocolEOKSingleApp'
    type_EOKSinglePart = 'epProtocolEOKSinglePart'
    type_EOKOU1 = 'epProtocolEOKOU1'
    type_EOKOU2 = 'epProtocolEOKOU2'
    type_EOKOU3 = 'epProtocolEOKOU3'
    type_EOKOUSingleApp = 'epProtocolEOKOUSingleApp'
    type_EOKOUSinglePart = 'epProtocolEOKOUSinglePart'
    type_EOKD1 = 'epProtocolEOKD1'
    type_EOKD2 = 'epProtocolEOKD2'
    type_EOKD3 = 'epProtocolEOKD3'
    type_EOKD4 = 'epProtocolEOKD4'
    type_EOKDSingleApp = 'epProtocolEOKDSingleApp'
    type_EOKDSinglePart = 'epProtocolEOKDSinglePart'
    type_EZK1 = 'epProtocolEZK1'
    type_EZK2 = 'epProtocolEZK2'
    type_EZP1 = 'epProtocolEZP1'
    type_EZP2 = 'epProtocolEZP2'
    type_EZP1Extract = 'epProtocolEZP1Extract'
