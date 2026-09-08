from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.core.mail import send_mail
from .models import Article, Subscriber, Photo
from .serializers import ArticleSerializer, PhotoSerializer, SubscriberSerializer
from .permissions import HasUploadKey

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('display_order', '-created_at')
    serializer_class = ArticleSerializer
    permission_classes = [HasUploadKey]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SubscriberViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def perform_create(self, serializer):
        subscriber = serializer.save()
        send_mail(
            subject='Welcome to [Your Blog Name]!',
            message="Thanks for subscribing! You'll get an email whenever a new post goes live.",
            from_email=None,
            recipient_list=[subscriber.email],
            fail_silently=False,
        )

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all().order_by('display_order', '-uploaded_at')
    serializer_class = PhotoSerializer