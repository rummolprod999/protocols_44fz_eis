from ClassProtocolOK2 import ProtocolOK2


class ProtocolOK1(ProtocolOK2):
    add_protocolOK1 = 0
    update_protocolOK1 = 0

    def __init__(self, protocol, xml):
        super().__init__(protocol, xml)
