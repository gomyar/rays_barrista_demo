import json

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

from barrista.models import Order
from barrista.models import Product
from barrista.mongodb import MongoDB
from barrista.container import Container

import jsonify

mongodb = MongoDB()
mongodb.init_mongo()
container = Container(mongodb)


def index(request):
    return render_to_response("index.html")


def orders(request):
    if request.method == "POST":
        order = container.create_order(request.POST['product_id'],
            request.POST['customer_name'])
        return HttpResponse(json.dumps(order, default=jsonify.encode),
            content_type="application/json")
    else:
        return HttpResponse(json.dumps(container.get_all_orders(),
            default=jsonify.encode), content_type="application/json")


def orders_byid(request, order_id):
    if request.method == "POST":
        container.order_complete(order_id)
        return HttpResponse("ok")
    else:
        return HttpResponse(json.dumps(container.get_order_by_id(order_id),
            default=jsonify.encode), content_type="application/json")


def products(request):
    product_dict = dict((p.product_id, p.name) for p in \
        container.get_all_products())
    return HttpResponse(json.dumps(product_dict, default=jsonify.encode),
        content_type="application/json")
