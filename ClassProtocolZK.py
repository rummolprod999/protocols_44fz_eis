import parser_prot
from ClassParticipiant import Participiant
from ClassProtocol import Protocol


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
