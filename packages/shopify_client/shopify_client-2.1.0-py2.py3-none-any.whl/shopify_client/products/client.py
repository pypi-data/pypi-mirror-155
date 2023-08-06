from .get import ProductGet
from .get_by_id import ProductGetById
from .metafields import MetafieldClient
from .update import ProductUpdate
from .variants import VariantClient


class ProductClient:
    @staticmethod
    def get(products_input):
        return ProductGet().get(products_input)

    @staticmethod
    def get_by_id(product_id):
        return ProductGetById().execute(product_id)

    @staticmethod
    def update(product_input):
        return ProductUpdate().get(product_input)

    @property
    def metafields(self):
        return MetafieldClient

    @property
    def variants(self):
        return VariantClient
