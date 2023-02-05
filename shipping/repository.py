from oscar.apps.shipping import repository
from . import methods

class Repository(repository.Repository):
    def get_available_shipping_methods(
            self, basket, user=None, shipping_addr=None,
            request=None, **kwargs):

        # Standard shipping 15€ per il lancio del prodotto         
        shipping = [methods.StandardShipping()]

        # shipping = [methods.NoShipping()]
        # if not shipping_addr:
        #     return [methods.NoShipping()]
        # # 'Hungary', 'Bulgaria', 'Estonia', 'Latvia', 'Lithuania', 'Romania'
        # EUROPE2_LIST = ['HU', 'BG', 'EE', 'LV', 'LT', 'RO']
        # # Italia 3.90
        # if shipping_addr and (shipping_addr.country.iso_3166_1_a2 and shipping_addr.country.iso_3166_1_a2.upper() == 'IT'):
        #     shipping = [methods.StandardItaly()]
        # elif shipping_addr and (shipping_addr.country.iso_3166_1_a2 and shipping_addr.country.iso_3166_1_a2.upper() in EUROPE2_LIST):
        #     # Se paese è: Ungheria, Bulgaria, Estonia, Lettonia, Lituania, Romania
        #     # StandardEurope2 7.90
        #     shipping = [methods.StandardEurope2()]
        # else:
        #     # Europa 5.90
        #     shipping = [methods.StandardEurope()]

        # # if basket.total_incl_tax >= 60:
        # #     shipping = [methods.Free()]
        # # else:
        # #     shipping = [methods.StandardEurope()]

        return shipping
