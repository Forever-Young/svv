import json
from urllib.request import pathname2url

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.db.models.expressions import F
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, Http404

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
        return PodcastIssue.objects.exclude(title__isnull=True).exclude(title__exact="").exclude(skip_feed=True)\
            .exclude(file__exact="").exclude(file__isnull=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_description

    def item_enclosure_url(self, item):
        return "http://{}{}".format(Site.objects.get_current(), item.get_file_url)

    def item_enclosure_length(self, item):
        return item.file.size

    def item_pubdate(self, item):
        return item.pub_date


class PodcastListView(ListView):
    paginate_by = settings.ISSUES_PER_PAGE
    queryset = PodcastIssue.objects.exclude(title__isnull=True).exclude(title__exact="")


class PodcastDetailView(DetailView):
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.file and obj.celery_task:
            obj.celery_task = ""
            obj.save()
        agent = self.request.META.get('HTTP_USER_AGENT', '').lower()
        bots = ('googlebot', 'yandex.com/bots', 'bingbot', 'adidxbot', 'msnbot', 'bingpreview')
        if not [bot for bot in bots if bot in agent]:
            PodcastIssue.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj

    def get_context_data(self, object):
        prev = next = None
        for pk in [item[0] for item in self.queryset.values_list('pk')]:
            if next:
                next = pk
                break
            if pk == object.pk:
                next = True
            else:
                prev = pk
        context = {'prev': prev, 'next': next}
        return super().get_context_data(**context)

    queryset = PodcastIssue.objects.exclude(title__isnull=True).exclude(title__exact="")


def order_converting(request, pk):
    obj = get_object_or_404(PodcastIssue, pk=pk)
    data = {"result": "ok"}
    if not obj.file:
        obj.celery_task = download_and_convert_task.delay(obj.pk, skip_feed=True)
        obj.save()
    return HttpResponse(json.dumps(data), content_type='application/json')


def check_converting_status(request, pk):
    obj = get_object_or_404(PodcastIssue, pk=pk)
    data = {}
    if obj.celery_task:
        result = download_and_convert_task.AsyncResult(obj.celery_task)
        if result.ready():
            if result.failed():
                if not obj.file:
                    data["result"] = "error"
                else:
                    data["result"] = "ok"
                    data["url"] = obj.file.url
                obj.celery_task = ""
                obj.save()
            else:
                data["result"] = "ok"
                data["url"] = obj.file.url
                obj.celery_task = ""
                obj.save()
        else:
            data["result"] = "not_ready"
    else:
        if not obj.file:
            data["result"] = "error"
        else:
            data["result"] = "ok"
            data["url"] = obj.file.url
    return HttpResponse(json.dumps(data), content_type='application/json')


def serve_file(request, pk):
    obj = get_object_or_404(PodcastIssue, pk=pk)
    if not obj.file:
        raise Http404
    PodcastIssue.objects.filter(pk=pk).update(views=F('views') + 1)
    response = HttpResponse()
    response["Content-Type"] = "audio/mpeg"
    response["Content-Disposition"] = "attachment; filename*=UTF-8*''{0}".format(pathname2url(obj.pretty_file_name.encode("utf-8")))
    response['X-Accel-Redirect'] = obj.file.url
    return response
