from django.conf.urls import patterns, include, url


urlpatterns = patterns('barrista.views',
    url(r'^$', 'index', name='index'),
    url(r'^make_order$', 'make_order', name='make_order'),
)
