from django.contrib import admin

from .models import PodcastIssue


def remove_skip_feed(modeladmin, request, queryset):
    for issue in queryset:
        issue.skip_feed = False
        issue.save()
remove_skip_feed.short_description = 'Remove skip feed mark from selected issues'


class PodcastIssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'last_view', 'downloaded', 'skip_feed')
    search_fields = ('title', 'youtube_url')

    def downloaded(self, obj):
        return bool(obj.file)
    downloaded.boolean = True

    actions = [remove_skip_feed]

admin.site.register(PodcastIssue, PodcastIssueAdmin)
