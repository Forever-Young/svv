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

    def _length_str(self, len):
        return ":".join([str(x).rjust(2, '0') for x in (len // 3600, (len % 3600) // 60, (len % 3600) % 60) if x > 0])\
            .lstrip('0')

    def video_length(self):
        return self._length_str(self.length_video)

    def audio_length(self):
        return self._length_str(self.length_audio)

    class Meta:
        ordering = ('-pub_date', '-title')
