
from barrista.models import Product
from barrista.models import Order


class Container(object):
    def __init__(self, dbase):
        self.dbase = dbase
        self.builders = dict(
            Product=self._build_product,
            Order=self._build_order,
        )

    def get_order_by_id(self, order_id):
        data = self.dbase.get_object("orders", order_id)
        return self.build(data)

    def get_product(self, product_id):
        data = self.dbase.find("products", product_id=product_id)
        return self.build(data)

    def build(self, data):
        if "__type__" in data:
            obj_type = data.pop('__type__')
            if obj_type in self.builders:
                return self.builders[obj_type](data)
            else:
                raise TypeError("No such type:%s" % obj_type)
        return data

    def _build_product(self, data):
        return Product(product_id=data['product_id'], name=data['name'])

    def _build_order(self, data):
        return Order(customer_name=data['customer_name'],
            product=self.get_product(data['product_id']))
