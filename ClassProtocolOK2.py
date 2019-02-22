import itertools

import parser_prot
from ClassParticipiant import Participiant
from ClassProtocol import Protocol


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
