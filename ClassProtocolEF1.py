import parser_prot
from ClassProtocol import Protocol


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
