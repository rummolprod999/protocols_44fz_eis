import parser_prot
from ClassParticipiant504 import Participiant504
from ClassProtocol504 import Protocol504


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
