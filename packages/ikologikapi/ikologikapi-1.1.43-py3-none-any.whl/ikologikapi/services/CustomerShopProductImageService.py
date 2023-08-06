import json
from types import SimpleNamespace

import requests

from ikologikapi.IkologikApiCredentials import IkologikApiCredentials
from ikologikapi.IkologikException import IkologikException
from ikologikapi.services.AbstractIkologikCustomerService import AbstractIkologikCustomerService


class CustomerShopProductImageService(AbstractIkologikCustomerService):

    def __init__(self, jwtHelper: IkologikApiCredentials):
        super().__init__(jwtHelper)

    # CRUD Actions

    def get_url(self, customer, shop_product) -> str:
        return f'{self.jwtHelper.get_url()}/api/v2/customer/{customer}/ shopproduct/{shop_product}/image'

    def get_by_id(self, customer: str, shop_product: str, id: str, include_upload_url: bool = False, include_download_url: bool = False, include_download_thumbnail_url: bool = False, include_download_view_url: bool = False) -> object:
        try:
            params = {'includeUploadUrl': include_upload_url,
                      'includeDownloadUrl': include_download_url,
                      'includeDownloadThumbnailUrl': include_download_thumbnail_url,
                      'includeDownloadViewUrl': include_download_view_url
                      }
            response = requests.get(
                self.get_url(customer, shop_product) + f'/{id}',
                params=params,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing get_by_id, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing get_by_id")

    def list(self, customer: str, shop_product: str, include_upload_url: bool = False, include_download_url: bool = False, include_download_thumbnail_url: bool = False, include_download_view_url: bool = False) -> list:
        try:
            params = {'includeUploadUrl': include_upload_url,
                      'includeDownloadUrl': include_download_url,
                      'includeDownloadThumbnailUrl': include_download_thumbnail_url,
                      'includeDownloadViewUrl': include_download_view_url
                      }
            response = requests.get(
                f'{self.get_url(customer, shop_product)}',
                params=params,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing list, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing list")

    def search(self, customer: str, shop_product: str, search, include_upload_url: bool = False, include_download_url: bool = False, include_download_thumbnail_url: bool = False, include_download_view_url: bool = False) -> list:
        try:
            params = {'includeUploadUrl': include_upload_url,
                      'includeDownloadUrl': include_download_url,
                      'includeDownloadThumbnailUrl': include_download_thumbnail_url,
                      'includeDownloadViewUrl': include_download_view_url
                      }
            data = json.dumps(search, default=lambda o: o.__dict__)
            response = requests.post(
                f'{self.get_url(customer, shop_product)}/search',
                params=params,
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing search, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing search")

    def create(self, customer: str, shop_product: str, o: object, include_upload_url: bool = False, include_download_url: bool = False, include_download_thumbnail_url: bool = False, include_download_view_url: bool = False) -> object:
        try:
            params = {'includeUploadUrl': include_upload_url,
                      'includeDownloadUrl': include_download_url,
                      'includeDownloadThumbnailUrl': include_download_thumbnail_url,
                      'includeDownloadViewUrl': include_download_view_url
                      }
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.post(
                self.get_url(customer, shop_product),
                params=params,
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 201:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing create, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing create")

    def update(self, customer: str, shop_product: str, o: object):
        try:
            data = json.dumps(o, default=lambda o: o.__dict__)
            response = requests.put(
                f'{self.get_url(customer, shop_product)}/{o.id}',
                data=data,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = json.loads(response.content, object_hook=lambda d: SimpleNamespace(**d))
                return result
            else:
                raise IkologikException("Error while performing update, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing update")

    def delete(self, customer: str, shop_product: str, id: str):
        try:
            response = requests.delete(
                f'{self.get_url(customer, shop_product)}/{id}',
                headers=self.get_headers()
            )
            if response.status_code != 204:
                raise IkologikException("Error while performing delete, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing delete")

    def upload(self, customer: str, shop_product: str, filename: str):
        try:
            params = {'filename': filename}
            response = requests.get(
                f'{self.get_url(customer, shop_product)}/upload',
                params=params,
                headers=self.get_headers()
            )
            if response.status_code == 200:
                result = response.content.decode("utf-8")
                return result
            else:
                raise IkologikException("Error while performing upload, the request returned status " + str(response.status_code))
        except IkologikException as ex:
            raise ex
        except Exception as ex:
            raise IkologikException("Error while performing upload")
