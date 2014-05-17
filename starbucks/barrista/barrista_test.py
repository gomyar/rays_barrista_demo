
from django.test import TestCase

from barrista.models import Product
from barrista.models import Order


class BarristaTest(TestCase):
    fixtures = ['barrista_test_fixtures/products.json']

    def setUp(self):
        pass

    def testMakeAnOrder(self):
        latte = Product.objects.get(product_id="latte")
        order = Order.objects.create(product=latte, customer_name="bob")

        self.assertEquals("Latte", order.product.name)

    def testMakeOrderThroughAPI(self):
        response = self.client.post("/orders", {"product_id": "latte",
            "customer_name": "bob"})
        self.assertEquals('{"product_id": 2, "customer_name": "bob"}',
            response.content)

        self.assertEquals(200, response.status_code)
        order = Order.objects.all()[0]

        self.assertEquals("Latte", order.product.name)

    def testGetOrders(self):
        latte = Product.objects.get(product_id="latte")
        Order.objects.create(product=latte, customer_name="bob")
        response = self.client.get("/orders")
        self.assertEquals('[{"product_id": 2, "customer_name": "bob"}]',
            response.content)
