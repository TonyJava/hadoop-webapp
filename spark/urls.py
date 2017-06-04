from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^content/$', views.content, name="content"),
    url(r'^check/$', views.check, name="check"),
    url(r'^phone/$', views.checkphone, name="phone"),
    url(r'^phonecontent/$', views.checkphonecontent, name="phonecontent"),
    url(r'^sms/$', views.checksms, name="sms"),
    url(r'^testphone/$', views.testphone, name="testphone"),
	url(r'^testsms/$', views.testsms, name="testsms"),
	url(r'^sparksms/$', views.sparksms, name="sparksms"),
]