import os
from itertools import dropwhile

from django.db import models
from django.core.urlresolvers import reverse

from .utils import sanitize


class PodcastIssue(models.Model):
    title = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    short_description = models.CharField(max_length=1000, null=True, blank=True)
    file = models.FileField(upload_to="mp3", null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    youtube_url = models.URLField()
    skip_feed = models.BooleanField(default=False)
    celery_task = models.CharField(max_length=40, null=True, blank=True)
    length_video = models.IntegerField(default=0)
    length_audio = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    last_view = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.youtube_url

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    def delete_file(self):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
            self.file = None
            self.save()

    @property
    def get_file_url(self):
        return reverse('download', args=[str(self.id)])

    @property
    def get_direct_file_url(self):
        return self.file.url

    @property
    def youtube_id(self):
        return self.youtube_url[self.youtube_url.rfind("=") + 1:]

    @staticmethod
    def _length_str(length):
        data = [str(x).rjust(2, '0') for x in (length // 3600, (length % 3600) // 60, (length % 3600) % 60)]
        data = list(dropwhile(lambda x: x == '00', data))
        if len(data) < 2:
            data.insert(0, '00')
        if len(data) < 2:
            data.insert(0, '00')
        if len(data[0]) > 1:
            data[0] = data[0].lstrip('0')
            if not data[0]:
                data[0] = '0'
        return ":".join(data)

    @property
    def video_length(self):
        return self._length_str(self.length_video)

    @property
    def audio_length(self):
        return self._length_str(self.length_audio)

    @property
    def pretty_file_name(self):
        return "{pub_date} {title} {youtube_id}".format(pub_date=self.pub_date.date(), title=sanitize(self.title),
                youtube_id=self.youtube_id)[:240] + ".mp3"

    class Meta:
        ordering = ('-pub_date', '-title')
