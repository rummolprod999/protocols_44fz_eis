import parser_prot
from ClassParticipiant504 import Participiant504
from ClassProtocol504 import Protocol504


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
