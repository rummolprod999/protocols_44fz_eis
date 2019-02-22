from ClassProtocolEOK2 import ProtocolEOK2


class ProtocolEOK1(ProtocolEOK2):
    add_protocolEOK1 = 0
    update_protocolEOK1 = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)
