import re

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps import GenericSitemap

from django.contrib import admin
admin.autodiscover()

from svv.views import (PodcastListView, PodcastDetailView, PodcastFeed,
                       order_converting, check_converting_status, serve_file)
from svv.models import PodcastIssue
from svv.sitemaps import StaticViewSitemap


sitemaps = {
    'static': StaticViewSitemap,
    'issues': GenericSitemap({'queryset': PodcastIssue.objects.all(), 'date_field': 'pub_date'}, priority=0.6),
}

urlpatterns = patterns('',
    url(r'^$', PodcastListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PodcastDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/download/$', serve_file, name='download'),
    url(r'^order-converting/(?P<pk>\d+)/$', order_converting, name='order-converting'),
    url(r'^check-converting-status/(?P<pk>\d+)/$', check_converting_status, name='check-converting-status'),
    url(r'^search/', include('haystack.urls')),
    url(r'^feed/$', PodcastFeed(), name='feed'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
