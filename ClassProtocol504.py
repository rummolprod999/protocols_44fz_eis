import dateutil.parser
import pytz

import UtilsFunctions


class Protocol504:
    def __init__(self, protocol, xml):
        prot = protocol[list(protocol.keys())[0]]
        list_p = [v for v in prot.keys() if v.lower().startswith("ep")]
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

    def get_print_form(self):
        d = UtilsFunctions.get_el(self.protocol, 'printFormInfo', 'url')
        if d.startswith("<![CDATA"):
            d = d[9:-3]
        return d

    def get_journal_number(self, application):
        d = UtilsFunctions.get_el(application, 'commonInfo', 'appNumber')
        return d
