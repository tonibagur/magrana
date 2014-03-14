from django.conf.urls import patterns, include, url
from views import views
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Pomelo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^youtube/', include('django_youtube.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), #{'template_name': 'myproject/shop_login.html','authentication_form':MyAuthenticationForm}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),# {'template_name': 'myproject/shop_logout.html'}),
    url(r'^demo_gift/', views.registerGift),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
