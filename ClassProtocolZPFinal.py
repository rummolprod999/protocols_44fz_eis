import parser_prot
from ClassProtocolEF3 import ProtocolEF3


class ProtocolZPFinal(ProtocolEF3):
    add_protocolZPFinal = 0
    update_protocolZPFinal = 0

    def get_price(self, application):
        d = parser_prot.get_el(application, 'lastOffer', 'price')
        return d
