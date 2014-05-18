
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

    def save_object(self, collection, data):
        new_id = "%s_%s" % (collection, len(self.collections[collection]))
        self.collections[collection][new_id] = data

    def find(self, collection, **kwargs):
        for obj in self.collections[collection].values():
            if all((k, v) in obj.items() for (k, v) in kwargs.items()):
                return obj
        return None


class ContainerTest(TestCase):
    fixtures = ['barrista_test_fixtures/products.json']

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

    def testSaveProduct(self):
        product = Product(product_id="prod1", name="Frappacino")
        self.container.save_product(product)

        self.assertEquals({'products_0': {'__type__': 'Product',
            'name': 'Frappacino', 'product_id': 'prod1'}},
            self.dbase.collections['products'])

    def testSaveOrder(self):
        self.dbase.collections['products']['product1'] = {
            "__type__": "Product", "product_id": "latte", "name": "Latte"}
        product = Product(product_id="latte", name="Latte")
        order = Order(product=product, customer_name="Ned")

        self.container.save_order(order)

        self.assertEquals({'orders_0': {'__type__': 'Order',
            'product_id': 'latte', 'customer_name': 'Ned'}},
            self.dbase.collections['orders'])

    def testGetObjectFromOldDbase(self):
        self.dbase.collections['products']['products_0'] = {
            "__type__": "Product", "product_id": "frap", "name": "Frappacino"}
        product_frap = self.container.get_product("frap")
        product_latte = self.container.get_product("latte")

        self.assertEquals("Frappacino", product_frap.name)
        self.assertEquals("Latte", product_latte.name)

    def testGetOrderFromOldDbase(self):
        self.dbase.collections['products']['products_0'] = {
            "__type__": "Product", "product_id": "frap", "name": "Frappacino"}
        self.dbase.collections['orders']['orders_0'] = {"__type__": "Order",
            "product_id": "latte", "customer_name": "Bob"}
        self.dbase.collections['orders']['orders_1'] = {"__type__": "Order",
            "product_id": "frap", "customer_name": "Ned"}

        order_bob = self.container.get_order_by_id("orders_0")
        order_ned = self.container.get_order_by_id("orders_1")

        self.assertEquals("Latte", order_bob.product.name)
        self.assertEquals("Bob", order_bob.customer_name)
        self.assertEquals("Frappacino", order_ned.product.name)
        self.assertEquals("Ned", order_ned.customer_name)
