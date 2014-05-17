
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
        response = self.client.post("/make_order", {"product_id": "latte"})

        self.assertEquals(200, response.status_code)
        order = Order.objects.all()[0]

        self.assertEquals("Latte", order.product.name)
