from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^content/$', views.content, name="content"),
    url(r'^check/$', views.check, name="check"),
]