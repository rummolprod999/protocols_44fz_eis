import dateutil.parser
import pytz
import json

import UtilsFunctions


class Protocol504:
    def __init__(self, protocol, xml):
        prot = protocol[list(protocol.keys())[0]]
        list_p = [v for v in prot.keys() if (v.lower().startswith("ep") or v.lower().startswith("pprf"))]
        self.protocol = prot[list_p[0]]
        self.xml = xml
        if 'protocolInfo' in self.protocol:
            if self.protocol['protocolInfo'] is None:
                self.applications = []
            elif 'applicationsInfo' in self.protocol['protocolInfo']:
                if 'applicationInfo' in self.protocol['protocolInfo']['applicationsInfo']:
                    self.applications = UtilsFunctions.generator_univ(
                            self.protocol['protocolInfo']['applicationsInfo']['applicationInfo'])
                else:
                    self.applications = []
            elif 'applicationInfo' in self.protocol['protocolInfo']:
                self.applications = UtilsFunctions.generator_univ(self.protocol['protocolInfo']['applicationInfo'])
            else:
                self.applications = []
        else:
            self.applications = []

    def get_purchaseNumber(self):
        d = UtilsFunctions.get_el(self.protocol, 'commonInfo', 'purchaseNumber')
        return d

    def get_id(self):
        d = UtilsFunctions.get_el(self.protocol, 'id')
        return d

    def get_protocol_date(self):
        d = UtilsFunctions.get_el(self.protocol, 'commonInfo', 'publishDTInEIS')
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
        d = UtilsFunctions.get_el(self.protocol, 'commonInfo', 'href')
        return d

    def get_url_external(self):
        d = UtilsFunctions.get_el(self.protocol, 'commonInfo', 'hrefExternal')
        return d

    def get_print_form(self):
        d = UtilsFunctions.get_el(self.protocol, 'printFormInfo', 'url') or UtilsFunctions.get_el(self.protocol,
                                                                                                  'extPrintFormInfo',
                                                                                                  'url')
        if d.startswith("<![CDATA"):
            d = d[9:-3]
        return d

    def get_print_form_ext(self):
        d = UtilsFunctions.get_el(self.protocol, 'extPrintFormInfo', 'url')
        if d.startswith("<![CDATA"):
            d = d[9:-3]
        return d

    def get_journal_number(self, application):
        d = UtilsFunctions.get_el(application, 'commonInfo', 'appNumber')
        return d

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
        dop_info = json.dumps(dop_info, sort_keys=False,
                              indent=4,
                              ensure_ascii=False,
                              separators=(',', ': '))
        return dop_info

    def get_abandoned_reason(self):
        d = UtilsFunctions.get_el(self.protocol, 'protocolInfo', 'abandonedReason', 'name') or UtilsFunctions.get_el(
            self.protocol, 'abandonedReason', 'name')
        k = UtilsFunctions.get_el(self.protocol, 'protocolInfo', 'abandonedReason', 'code') or UtilsFunctions.get_el(
            self.protocol, 'abandonedReason', 'name')
        if d and k:
            return f'{d}|{k}'
        return d or k
