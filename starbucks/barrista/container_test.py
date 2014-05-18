
from django.test import TestCase
from pymongo.helpers import bson

from container import Container
from barrista.models import Order
from barrista.models import Product


class MockMongo(object):
    def __init__(self):
        self.collections = dict(
            orders=dict(),
            products=dict(),
        )

    def get_object(self, collection_name, object_id):
        return self.collections[collection_name][object_id]

    def save_object(self, collection_name, data):
        new_id = "%s_%s" % (collection_name,
            len(self.collections[collection_name]))
        self.collections[collection_name][new_id] = data
        return new_id

    def find_one(self, collection_name, **kwargs):
        found = self.find(collection_name, **kwargs)
        if found:
            return found[0]
        else:
            return None

    def find(self, collection_name, **kwargs):
        found = []
        for obj in self.collections[collection_name].values():
            if all((k, v) in obj.items() for (k, v) in kwargs.items()):
                found.append(obj)
        found = [f.copy() for f in found]
        return found

    def object_exists(self, collection_name, object_id):
        return object_id in self.collections[collection_name]

    def remove_object(self, collection_name, object_id):
        self.collections[collection_name].pop(object_id)


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
        self.assertTrue(self.container.order_exists('orders_0'))

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

    def testGetAllOrders(self):
        self.dbase.collections['orders']['orders_0'] = {"__type__": "Order",
            "product_id": "latte", "customer_name": "Ned"}
        self.dbase.collections['orders']['orders_1'] = {"__type__": "Order",
            "product_id": "cappacino", "customer_name": "Bob"}

        self.assertEquals(2, len(self.container.get_all_orders()))
        self.assertEquals(2, len(self.container.get_all_products()))

        product = Product.objects.create(product_id="prod1", name="Frappacino")
        Order.objects.create(product=product, customer_name="Bill")

        self.assertEquals(3, len(self.container.get_all_orders()))
        self.assertEquals(3, len(self.container.get_all_products()))

        self.dbase.collections['products']['products_0'] = {
            "__type__": "Product", "product_id": "frap", "name": "Frappacino"}

        self.assertEquals(3, len(self.container.get_all_orders()))
        self.assertEquals(4, len(self.container.get_all_products()))

    def testRemoveOrder(self):
        self.dbase.collections['orders']['orders_0'] = {"__type__": "Order",
            "product_id": "latte", "customer_name": "Bob"}

        self.container.remove_order("orders_0")

        self.assertEquals(0, len(self.dbase.collections['orders']))

    def testMigrate(self):
        self.dbase.collections['orders']['orders_0'] = {"__type__": "Order",
            "product_id": "latte", "customer_name": "Ned"}
        self.dbase.collections['orders']['orders_1'] = {"__type__": "Order",
            "product_id": "cappacino", "customer_name": "Bob"}
        self.dbase.collections['products']['products_0'] = {
            "__type__": "Product", "product_id": "mocha", "name": "Mocha"}
        product = Product.objects.create(product_id="prod1", name="Frappacino")
        Order.objects.create(product=product, customer_name="Bill")

        self.assertEquals(2, len(self.dbase.collections['orders']))
        self.assertEquals(1, len(Order.objects.all()))
        self.assertEquals(1, len(self.dbase.collections['products']))
        self.assertEquals(3, len(Product.objects.all()))

        self.container.migrate()

        self.assertEquals(3, len(self.dbase.collections['orders']))
        self.assertEquals(0, len(Order.objects.all()))
        self.assertEquals(4, len(self.dbase.collections['products']))
        self.assertEquals(0, len(Product.objects.all()))

    def testOddObjectIdBug(self):
        self.dbase.collections['products']['5378cefd2e594f10a0000000'] = {
            "_id": bson.ObjectId("5378cefd2e594f10a0000000"),
            "__type__": "Product", "product_id": "mocha", "name": "Mocha"}
        self.dbase.collections['orders']['5378cefd2e594f10a0000001'] = {
            "__type__": "Order",
            "_id": bson.ObjectId("5378cefd2e594f10a0000001"),
            "product_id": "latte", "customer_name": "Ned"}

        self.assertEquals("Mocha", self.container.get_product("mocha").name)
        self.assertEquals("Ned",
            self.container.get_order_by_id("5378cefd2e594f10a0000001").customer_name)


    def testOldObjectExistsWithOldId(self):
        self.assertFalse(self.container.order_exists("1"))
