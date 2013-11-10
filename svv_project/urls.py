from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from svv.views import PodcastListView, PodcastDetailView, PodcastFeed, order_converting, check_converting_status

urlpatterns = patterns('',
    url(r'^$', PodcastListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PodcastDetailView.as_view(), name='detail'),
    url(r'^feed/$', PodcastFeed(), name='feed'),
    url(r'^order-converting/(?P<pk>\d+)/$', order_converting, name='order-converting'),
    url(r'^check-converting-status/(?P<pk>\d+)/$', check_converting_status, name='check-converting-status'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
