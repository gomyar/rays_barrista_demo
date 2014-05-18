
from django.test import TestCase

from container import Container
from barrista.models import Order
from barrista.models import Product


class MockMongo(object):
    def __init__(self):
        self.collections = dict(
            orders=dict(),
            products=dict(),
        )

    def get_object(self, collection, object_id):
        return self.collections[collection][object_id]

    def find(self, collection, **kwargs):
        for obj in self.collections[collection].values():
            if all((k, v) in obj.items() for (k, v) in kwargs.items()):
                return obj
        return None


class ContainerTest(TestCase):
    def setUp(self):
        self.dbase = MockMongo()
        self.container = Container(self.dbase)

    def testBuildProduct(self):
        self.dbase.collections['products']['product1'] = {
            "__type__": "Product", "product_id": "latte", "name": "Latte"}
        product = self.container.get_product("latte")
        self.assertEquals(Product, type(product))
        self.assertEquals("Latte", product.name)

    def testBuildOrder(self):
        self.dbase.collections['products']['product1'] = {
            "__type__": "Product", "product_id": "latte", "name": "Latte"}
        self.dbase.collections['orders']['order1'] = {"__type__": "Order",
            "product_id": "latte", "customer_name": "Bob"}
        order = self.container.get_order_by_id("order1")
        self.assertEquals(Order, type(order))
        self.assertEquals("latte", order.product.product_id)
        self.assertEquals("Bob", order.customer_name)
