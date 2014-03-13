from django.conf.urls import patterns, include, url
from views import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Pomelo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^demo_gift', views.registerGift),
    url(r'^admin/', include(admin.site.urls)),
)
