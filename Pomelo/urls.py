from django.conf.urls import patterns, include, url
from views import views
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from views.views import MyResponseView, GiftView
admin.autodiscover()

urlpatterns = patterns('',
    # phone app
    url(r'^fetch-youtube-data.json$', MyResponseView.as_view(), {'action': 'get_youtube_data'}),
    url(r'^gift_form/$', GiftView.as_view(), name='djng_gift_form'),
    

    (r'^youtube/', include('django_youtube.urls')),
    url(r'^$', login_required(views.home, login_url='/accounts/login/'), name='home'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),# {'template_name': 'myproject/shop_logout.html'}),
    #url(r'^demo_gift/story', login_required(views.views_gifts, login_url='/accounts/login/'), name='gift_story'),
    url(r'^demo_gift/', login_required(views.register_gift, login_url='/accounts/login/'), name='demo_gift'),
    url(r'^save_draft/', login_required(views.save_draft, login_url='/account/login'), name='save_draft'),
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
