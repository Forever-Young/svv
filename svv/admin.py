from django.contrib import admin

from .models import PodcastIssue


class PodcastIssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'views')
    search_fields = ('title', 'youtube_url')


admin.site.register(PodcastIssue, PodcastIssueAdmin)
