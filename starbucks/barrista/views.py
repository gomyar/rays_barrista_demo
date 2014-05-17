from django.shortcuts import render
from django.http import HttpResponse

from barrista.models import Order
from barrista.models import Product


def index(request):
    return HttpResponse("Welcome to Starbucks")


def make_order(request):
    product = Product.objects.get(product_id=request.POST['product_id'])
    Order.objects.create(product=product)
    return HttpResponse("Done")
