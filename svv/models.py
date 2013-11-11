from itertools import dropwhile

from django.db import models
from django.core.urlresolvers import reverse


class PodcastIssue(models.Model):
    # if blank - youtube_url should be filled to store processed urls
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

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.youtube_url

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    def youtube_id(self):
        return self.youtube_url[self.youtube_url.rfind("=") + 1:]

    def _length_str(self, length):
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

    def video_length(self):
        return self._length_str(self.length_video)

    def audio_length(self):
        return self._length_str(self.length_audio)

    class Meta:
        ordering = ('-pub_date', '-title')
