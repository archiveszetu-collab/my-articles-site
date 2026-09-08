from django.db import models
from django.core.mail import send_mass_mail
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    source_url = models.URLField(blank=True, null=True)
    cover_image = models.URLField(max_length=1000, blank=True, null=True)
    notified = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def notify_subscribers(self):
        if self.notified:
            return
        subscribers = Subscriber.objects.all()
        if not subscribers.exists():
            return

        messages = [
            (
                f'New post: {self.title}',
                f'A new article just went live: {self.title}\n\nRead it here: http://localhost:3000/articles/{self.id}',
                settings.DEFAULT_FROM_EMAIL,
                [sub.email],
            )
            for sub in subscribers
        ]
        send_mass_mail(messages, fail_silently=False)
        self.notified = True
        self.save(update_fields=['notified'])


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Photo(models.Model):
    title = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    image = models.CharField(max_length=1000)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    display_order = models.IntegerField(default=0)

    def __str__(self):
        return self.title or f"Photo {self.id}"