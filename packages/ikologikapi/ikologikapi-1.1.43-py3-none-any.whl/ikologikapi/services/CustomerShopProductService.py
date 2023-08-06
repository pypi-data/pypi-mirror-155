from ikologikapi.IkologikApiCredentials import IkologikApiCredentials
from ikologikapi.services.AbstractIkologikCustomerService import AbstractIkologikCustomerService


class CustomerShopProductService(AbstractIkologikCustomerService):

    def __init__(self, jwtHelper: IkologikApiCredentials):
        super().__init__(jwtHelper)

    # CRUD Actions

    def get_url(self, customer) -> str:
        return f'{self.jwtHelper.get_url()}/api/v2/customer/{customer}/shopproduct'
