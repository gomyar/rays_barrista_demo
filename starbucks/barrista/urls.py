from django.conf.urls import patterns, include, url


urlpatterns = patterns('barrista.views',
    url(r'^$', 'index', name='index'),
    url(r'^orders$', 'orders', name='orders'),
    url(r'^orders/(?P<order_id>[\w]*)$', 'orders_byid', name='orders_byid'),
    url(r'^products$', 'products', name='products'),
    url(r'^migrate$', 'migrate', name='migrate'),
)
