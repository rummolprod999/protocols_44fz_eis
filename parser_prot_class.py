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


class Type_protocol:
    type_EF1 = 'ProtocolEF1'
    type_EF2 = 'ProtocolEF2'
    type_EF3 = 'ProtocolEF3'
    type_ZK = 'ProtocolZK'
    type_ZKAfterProlong = 'ZKAfterProlong'
    type_EFSingleApp = 'ProtocolEFSingleApp'
    type_EFSinglePart = 'ProtocolEFSinglePart'
    type_OK2 = 'ProtocolOK2'
    type_OKD5 = 'ProtocolOKD5'
    type_OKOU3 = 'ProtocolOKOU3'
    type_ZPFinal = 'ProtocolZPFinal'
    type_Deviation = 'ProtocolDeviation'
    type_EFInvalidation = 'ProtocolEFInvalidation'
    type_OKSingleApp = 'ProtocolOKSingleApp'
    type_OKDSingleApp = 'ProtocolOKDSingleApp'
    type_OKOUSingleApp = 'ProtocolOKOUSingleApp'
    type_OK1 = 'ProtocolOK1'
    type_OKD1 = 'ProtocolOKD1'
    type_OKD2 = 'ProtocolOKD2'
    type_OKD3 = 'ProtocolOKD3'
    type_OKD4 = 'ProtocolOKD4'
    type_OKOU1 = 'ProtocolOKOU1'
    type_OKOU2 = 'ProtocolOKOU2'
    type_Cancel = 'ProtocolCancel'


class Type_protocol504:
    type_EOK1 = 'epProtocolEOK1'
    type_EOK2 = 'epProtocolEOK2'
    type_EOK3 = 'epProtocolEOK3'
    type_EOKSingleApp = 'epProtocolEOKSingleApp'
    type_EOKSinglePart = 'epProtocolEOKSinglePart'
    type_EOKOU1 = 'epProtocolEOKOU1'
    type_EOKOU2 = 'epProtocolEOKOU2'
    type_EOKOU3 = 'epProtocolEOKOU3'
    type_EOKOUSingleApp = 'epProtocolEOKOUSingleApp'
    type_EOKOUSinglePart = 'epProtocolEOKOUSinglePart'
    type_EOKD1 = 'epProtocolEOKD1'
    type_EOKD2 = 'epProtocolEOKD2'
    type_EOKD3 = 'epProtocolEOKD3'
    type_EOKD4 = 'epProtocolEOKD4'
    type_EOKDSingleApp = 'epProtocolEOKDSingleApp'
    type_EOKDSinglePart = 'epProtocolEOKDSinglePart'
    type_EZK1 = 'epProtocolEZK1'
    type_EZK2 = 'epProtocolEZK2'
    type_EZP1 = 'epProtocolEZP1'
    type_EZP2 = 'epProtocolEZP2'
    type_EZP1Extract = 'epProtocolEZP1Extract'
