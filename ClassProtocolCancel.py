import dateutil.parser
import pytz

import parser_prot
from ClassProtocol import Protocol


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
