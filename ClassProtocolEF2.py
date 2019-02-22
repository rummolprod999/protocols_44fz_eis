import parser_prot
from ClassProtocol import Protocol


class ProtocolEF2(Protocol):
    add_protocolEF2 = 0
    update_protocolEF2 = 0

    def get_offer_first_price(self, application):
        d = parser_prot.get_el(application, 'priceOffers', 'firstOffer', 'price')
        if not d:
            d = 0.0
        return d

    def get_offer_last_price(self, application):
        d = parser_prot.get_el(application, 'priceOffers', 'lastOffer', 'price')
        if not d:
            d = 0.0
        return d

    def get_offer_quantity(self, application):
        d = parser_prot.get_el(application, 'priceOffers', 'offersQuantity')
        if not d:
            d = 0
        return d
