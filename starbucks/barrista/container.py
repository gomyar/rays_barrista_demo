
import json

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
            return self.dict_to_obj(data)

    def get_all_products(self):
        return Product.objects.all()

    def get_all_orders(self):
        old_orders = list(Order.objects.all())
        order_data = self.dbase.find("orders")
        order_data = [self._decode_id(order) for order in order_data]
        new_orders = self.dict_to_obj(order_data)
        return old_orders + new_orders

    def remove_order(self, order_id):
        self.dbase.remove_object("orders", order_id)

    def create_order(self, product_id, customer_name):
        product = self.get_product(product_id)
        order = Order(product=product, customer_name=customer_name)
        self.save_order(order)
        return order

    def order_complete(self, order_id):
        if self.order_exists(order_id):
            self.remove_order(order_id)
        else:
            order = Order.objects.get(id=int(order_id))
            order.delete()

    def _decode_id(self, data):
        data['_id'] = str(data.get('_id'))
        return data

    def order_exists(self, order_id):
        return self.dbase.object_exists('orders', order_id)

    def save_order(self, order):
        self.save_object("orders", order)

    def save_object(self, collection_name, obj):
        data = self.obj_to_dict(obj)
        obj._id = self.dbase.save_object(collection_name, data)

    def get_product(self, product_id):
        data = self.dbase.find_one("products", product_id=product_id)
        if not data:
            return Product.objects.get(product_id=product_id)
        else:
            return self.dict_to_obj(data)

    def save_product(self, product):
        self.save_object("products", product)

    def obj_to_dict(self, pyobject):
        encoded_str = json.dumps(pyobject, default=self.serialize, indent=4)
        return json.loads(encoded_str)

    def dict_to_obj(self, obj_dict):
        obj_str = json.dumps(obj_dict)
        return json.loads(obj_str, object_hook=self.build)

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
        order = Order(customer_name=data['customer_name'],
            product=self.get_product(data['product_id']))
        order._id = data.get('_id')
        return order

    def _serialize_product(self, product):
        return dict(product_id=product.product_id, name=product.name)

    def _serialize_order(self, order):
        return dict(product_id=order.product.product_id,
            customer_name=order.customer_name)
