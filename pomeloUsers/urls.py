from django.conf.urls import patterns, url
from pomeloUsers import views

urlpatterns = patterns('',
    url(r'^$', views.registerGift, name='form')
)
