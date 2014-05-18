
from django.test import TestCase

from barrista.models import Product
from barrista.models import Order
from barrista import views
from barrista.container_test import MockMongo
from barrista.container import Container


class BarristaTest(TestCase):
    fixtures = ['barrista_test_fixtures/products.json']

    def setUp(self):
        self.dbase = MockMongo()
        views.container = Container(self.dbase)
        self.dbase.collections['products']['products_0'] = {
            "__type__": "Product", "product_id": "latte", "name": "Latte"}
        self.dbase.collections['products']['products_1'] = {
            "__type__": "Product", "product_id": "cappacino",
            "name": "Cappacino"}

    def testMakeAnOrder(self):
        latte = Product.objects.get(product_id="latte")
        order = Order.objects.create(product=latte, customer_name="bob")

        self.assertEquals("Latte", order.product.name)

    def testMakeOrderThroughAPI(self):
        response = self.client.post("/orders", {"product_id": "latte",
            "customer_name": "bob"})
        self.assertEquals(
            '{"order_id": "orders_0", "product_id": "latte", '
            '"customer_name": "bob"}',
            response.content)

        self.assertEquals(200, response.status_code)
        order = views.container.get_order_by_id("orders_0")

        self.assertEquals("Latte", order.product.name)

    def testGetOrders(self):
        latte = Product.objects.get(product_id="latte")
        Order.objects.create(product=latte, customer_name="bob")
        response = self.client.get("/orders")
        self.assertEquals(
            '[{"order_id": "1", "product_id": "latte", "customer_name": "bob"}]',
            response.content)

    def testGetProducts(self):
        self.assertEquals('{"cappacino": "Cappacino", "latte": "Latte"}',
            self.client.get("/products").content)

    def testOrderServed(self):
        latte = Product.objects.get(product_id="latte")
        Order.objects.create(product=latte, customer_name="bob")
        response = self.client.post("/orders/1", {"action": "served"})
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, len(Order.objects.all()))

    def testNewOrderServed(self):
        self.dbase.collections['orders']['orders_0'] = {"__type__": "Order",
            "product_id": "latte", "customer_name": "Bob"}

        response = self.client.post("/orders/orders_0", {"action": "served"})
        self.assertEquals(200, response.status_code)

        self.assertEquals(0, len(self.dbase.collections['orders']))
