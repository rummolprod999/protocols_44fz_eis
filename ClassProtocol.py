import dateutil.parser
import pytz
import json

import UtilsFunctions


class Protocol:
    def __init__(self, protocol, xml):
        prot = protocol[list(protocol.keys())[0]]
        list_p = [v for v in prot.keys() if 'fcs' in v.lower()]
        self.protocol = prot[list_p[0]]
        self.xml = xml
        if 'protocolLot' in self.protocol:
            if self.protocol['protocolLot'] is None:
                self.applications = []
            elif 'applications' in self.protocol['protocolLot']:
                if 'application' in self.protocol['protocolLot']['applications']:
                    self.applications = UtilsFunctions.generator_univ(
                            self.protocol['protocolLot']['applications']['application'])
                else:
                    self.applications = []
            elif 'application' in self.protocol['protocolLot']:
                self.applications = UtilsFunctions.generator_univ(self.protocol['protocolLot']['application'])
            else:
                self.applications = []
        else:
            self.applications = []

    def get_purchaseNumber(self):
        d = UtilsFunctions.get_el(self.protocol, 'purchaseNumber')
        return d

    def get_id(self):
        d = UtilsFunctions.get_el(self.protocol, 'id')
        return d

    def get_protocol_date(self):
        d = UtilsFunctions.get_el(self.protocol, 'protocolDate')
        if d:
            try:
                dt = dateutil.parser.parse(d)
                d = dt.astimezone(pytz.timezone("Europe/Moscow"))
            except Exception:
                d = ''
        else:
            d = ''
        return str(d)

    def get_url(self):
        d = UtilsFunctions.get_el(self.protocol, 'href')
        return d

    def get_print_form(self):
        d = UtilsFunctions.get_el(self.protocol, 'printForm', 'url')
        if d.startswith("<![CDATA"):
            d = d[9:-3]
        return d

    def get_journal_number(self, application):
        d = UtilsFunctions.get_el(application, 'journalNumber')
        return d

    def get_url_external(self):
        d = UtilsFunctions.get_el(self.protocol, 'commonInfo', 'hrefExternal')
        return d

    def get_print_form_ext(self):
        try:
            d = UtilsFunctions.get_el_list(self.protocol, 'attachments', 'attachment')

            if len(d) > 0:
                d = UtilsFunctions.get_el(d[0], 'url')
                if d:
                    return d
        except:
            d = UtilsFunctions.get_el(self.protocol, 'attachments', 'attachment', 'url')
            if d:
                return d
        d = UtilsFunctions.get_el(self.protocol, 'extPrintFormInfo', 'url')
        if d.startswith("<![CDATA"):
            d = d[9:-3]
        return d

    def get_abandoned_reason(self):
        d = UtilsFunctions.get_el(self.protocol, 'protocolLot', 'abandonedReason', 'name')
        k = UtilsFunctions.get_el(self.protocol, 'protocolLot', 'abandonedReason', 'code')
        if d and k:
            return f'{d}|{k}'
        return d or k

    def get_dop_info(self, p):
        dop_info = p.protocol
        try:
            del dop_info['extPrintFormInfo']['signature']
        except:
            pass
        try:
            del dop_info['attachmentsInfo']['attachmentInfo']['cryptoSigns']
        except:
            try:
                for e in dop_info['attachmentsInfo']['attachmentInfo']:
                    del e['cryptoSigns']
            except:
                pass
        try:
            del dop_info['extPrintFormInfo']['commissionSignatures']
        except:
            pass
        try:
            del dop_info['attachmentsInfo']['attachmentInfo']['cryptoSigns']
        except:
            try:
                for e in dop_info['attachmentsInfo']['attachmentInfo']:
                    del e['cryptoSigns']
            except:
                pass
        dop_info = json.dumps(dop_info, sort_keys=False,
                              indent=4,
                              ensure_ascii=False,
                              separators=(',', ': '))
        return dop_info
