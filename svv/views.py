import json

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from svv.models import PodcastIssue


class PodcastFeed(Feed):
    title = "SiliconValleyVoice"
    link = "https://www.youtube.com/user/SiliconValleyVoice/videos"
    description = "SiliconValleyVoice MP3 files."
    author_name = "Mikhail Portnov"
    item_enclosure_mime_type = "audio/mpeg"

    def items(self):
        return PodcastIssue.objects.exclude(title__isnull=True).exclude(skip_feed=True)\
            .exclude(file__exact="").exclude(file__isnull=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_enclosure_url(self, item):
        return item.file.url

    def item_enclosure_length(self, item):
        return item.file.size

    def item_pubdate(self, item):
        return item.pub_date


class PodcastListView(ListView):
    paginate_by = 6
    queryset = PodcastIssue.objects.exclude(title__isnull=True)


class PodcastDetailView(DetailView):
    queryset = PodcastIssue.objects.exclude(title__isnull=True)


def order_converting(request, pk):
    object = get_object_or_404(PodcastIssue, pk=pk)
    data = {"result": "ok"}
    if not object.file:
        from .tasks import download_and_convert_task
        download_and_convert_task.delay(object.pk)
    return HttpResponse(json.dumps(data), content_type='application/json')


def check_converting_status(request, pk):
    # FIXME: check for task result, so can return 'error' to browser if video can't be downloaded
    object = get_object_or_404(PodcastIssue, pk=pk)
    data = {}
    if not object.file:
        data["result"] = "not_ready"
    else:
        data["result"] = "ok"
        data["url"] = object.file.url
    return HttpResponse(json.dumps(data), content_type='application/json')
