from django.contrib import admin

from .models import PodcastIssue


class PodcastIssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'last_view', 'downloaded', 'skip_feed')
    search_fields = ('title', 'youtube_url')

    def downloaded(self, obj):
        return bool(obj.file)
    downloaded.boolean = True

admin.site.register(PodcastIssue, PodcastIssueAdmin)
