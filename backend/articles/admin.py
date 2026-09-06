from django.contrib import admin
from .models import Article, Subscriber

@admin.action(description='Notify subscribers about selected articles')
def notify_subscribers(modeladmin, request, queryset):
    for article in queryset:
        article.notify_subscribers()

class ArticleAdmin(admin.ModelAdmin):
    actions = [notify_subscribers]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Subscriber)