import parser_prot
import xmltodict

from ClassTypeProtocols504 import TypeProtocols504
from ClassTypeProtocols import TypeProtocols

file_name = "/home/alex/PycharmProjects/protocols_44fz_eis/epProtocolDeviation_0373100016122000008_36808218.xml"
with open(file_name) as fd:
    try:
        firs_str = fd.read()
        if True:
            firs_str = firs_str.replace("xmlns:ns1", "xmlnsns1").replace("xmlns:ns2", "xmlnsns2").replace(
                    "xmlns:ns3", "xmlnsns3").replace("xmlns:ns4", "xmlnsns4") \
                .replace("xmlns:ns5", "xmlnsns5").replace("xmlns:ns6", "xmlnsns6").replace("xmlns:ns7",
                                                                                           "xmlnsns7").replace(
                    "xmlns:ns8", "xmlnsns8").replace(
                    "xmlns:ns9", "xmlnsns9")
            firs_str = firs_str.replace("ns1:", "").replace("ns2:", "").replace("ns3:", "").replace("ns4:", "") \
                .replace("ns5:", "").replace("ns6:", "").replace("ns7:", "").replace("ns8:", "").replace("ns9:", "")
        doc = xmltodict.parse(firs_str)
        parser_prot.parser(doc, file_name,
                           file_name, 32,
                           TypeProtocols504.type_epProtocolDeviation)
    except Exception as ex:
        print(ex)
