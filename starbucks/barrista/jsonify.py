
from barrista.models import Order
from barrista.models import Product


def encode(obj):
    if type(obj) is Order:
        return dict(
            product_id=obj.product.product_id,
            customer_name=obj.customer_name,
            order_id=obj.order_id,
        )
    if type(obj) is Product:
        return dict(
            product_id=obj.product_id,
            name=obj.name,
        )
    else:
        return obj

