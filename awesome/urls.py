from django.conf.urls import include, url
from django.contrib import admin

from awesome.views import graph_view, graph

urlpatterns = [
    url(r'^$', graph_view, name="graph_view"),
    url(r'^api/graph/$', graph, name="api_hello")
]

