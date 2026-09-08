from rest_framework import serializers
from .models import Article, Photo, Subscriber

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'views', 'featured', 'source_url', 'cover_image','display_order']


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'subscribed_at']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title', 'caption', 'image', 'uploaded_at', 'display_order']