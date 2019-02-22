import parser_prot
from ClassParticipiant504 import Participiant504
from ClassProtocol504 import Protocol504


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
