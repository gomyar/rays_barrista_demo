import json

from django.shortcuts import render
from django.http import HttpResponse

from barrista.models import Order
from barrista.models import Product


def jsonify(obj):
    if type(obj) is Order:
        return dict(
            product_id=obj.product_id,
            customer_name=obj.customer_name,
        )
    else:
        return obj


def index(request):
    return HttpResponse("Welcome to Starbucks")


def orders(request):
    if request.method == "POST":
        product = Product.objects.get(product_id=request.POST['product_id'])
        order = Order.objects.create(product=product,
            customer_name=request.POST['customer_name'])
        return HttpResponse(json.dumps(order, default=jsonify))
    else:
        return HttpResponse(json.dumps(list(Order.objects.all()),
            default=jsonify))
