import json

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

from barrista.models import Order
from barrista.models import Product


def jsonify(obj):
    if type(obj) is Order:
        return dict(
            product_id=obj.product.product_id,
            customer_name=obj.customer_name,
            order_id=str(obj.id),
        )
    if type(obj) is Product:
        return dict(
            product_id=obj.product_id,
            name=obj.name,
            order_id=str(obj.id),
        )
    else:
        return obj


def index(request):
    return render_to_response("index.html")


def orders(request):
    if request.method == "POST":
        product = Product.objects.get(product_id=request.POST['product_id'])
        order = Order.objects.create(product=product,
            customer_name=request.POST['customer_name'])
        return HttpResponse(json.dumps(order, default=jsonify),
            content_type="application/json")
    else:
        return HttpResponse(json.dumps(list(Order.objects.all()),
            default=jsonify), content_type="application/json")


def orders_byid(request, order_id):
    order = Order.objects.get(id=int(order_id))
    order.delete()
    return HttpResponse("ok")


def products(request):
    product_dict = dict((p.product_id, p.name) for p in Product.objects.all())
    return HttpResponse(json.dumps(product_dict, default=jsonify),
        content_type="application/json")
