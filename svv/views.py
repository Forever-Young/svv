import json

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from .models import PodcastIssue
from .tasks import download_and_convert_task


class PodcastFeed(Feed):
    title = "SiliconValleyVoice"
    link = "/"
    feed_url = "/feed/"
    description = "SiliconValleyVoice в MP3".encode("utf-8")
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
        object.celery_task = download_and_convert_task.delay(object.pk)
        object.save()
    return HttpResponse(json.dumps(data), content_type='application/json')


def check_converting_status(request, pk):
    object = get_object_or_404(PodcastIssue, pk=pk)
    data = {}
    if object.celery_task:
        result = download_and_convert_task.AsyncResult(object.celery_task)
        if result:
            if result.ready():
                if result.get():
                    data["result"] = "ok"
                    data["url"] = object.file.url
                    object.celery_task = ""
                    object.save()
                else:
                    data["result"] = "error"
            else:
                data["result"] = "not_ready"
        else:
            data["result"] = "error"
    else:
        if not object.file:
            data["result"] = "not_ready"
        else:
            data["result"] = "ok"
            data["url"] = object.file.url
    return HttpResponse(json.dumps(data), content_type='application/json')
