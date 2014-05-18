
from barrista.models import Product
from barrista.models import Order


class Container(object):
    def __init__(self, dbase):
        self.dbase = dbase
        self.builders = dict(
            Product=self._build_product,
            Order=self._build_order,
        )
        self.serializers = dict(
            Product=self._serialize_product,
            Order=self._serialize_order,
        )

    def get_order_by_id(self, order_id):
        data = self.dbase.get_object("orders", order_id)
        if not data:
            return Order.objects.get(id=int(order_id))
        else:
            return self.build(data)

    def save_order(self, order):
        data = self.serialize(order)
        self.dbase.save_object("orders", data)

    def get_product(self, product_id):
        data = self.dbase.find("products", product_id=product_id)
        if not data:
            return Product.objects.get(product_id=product_id)
        else:
            return self.build(data)

    def save_product(self, product):
        data = self.serialize(product)
        self.dbase.save_object("products", data)

    def build(self, data):
        if "__type__" in data:
            obj_type = data.pop('__type__')
            if obj_type in self.builders:
                return self.builders[obj_type](data)
            else:
                raise TypeError("No such type:%s" % obj_type)
        return data

    def serialize(self, obj):
        obj_name =  type(obj).__name__
        if obj_name in self.serializers:
            data = self.serializers[obj_name](obj)
            data['__type__'] = obj_name
            return data
        raise TypeError("Cannot serialize object %s" % obj_name)

    def _build_product(self, data):
        return Product(product_id=data['product_id'], name=data['name'])

    def _build_order(self, data):
        return Order(customer_name=data['customer_name'],
            product=self.get_product(data['product_id']))

    def _serialize_product(self, product):
        return dict(product_id=product.product_id, name=product.name)

    def _serialize_order(self, order):
        return dict(product_id=order.product.product_id,
            customer_name=order.customer_name)
