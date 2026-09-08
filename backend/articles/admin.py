from django.contrib import admin
from .models import Article, Subscriber, Photo

@admin.action(description='Notify subscribers about selected articles')
def notify_subscribers(modeladmin, request, queryset):
    for article in queryset:
        article.notify_subscribers()

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'display_order']
    ordering = ['display_order', '-uploaded_at']

admin.site.register(Photo, PhotoAdmin)

class ArticleAdmin(admin.ModelAdmin):
    actions = [notify_subscribers]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Subscriber)