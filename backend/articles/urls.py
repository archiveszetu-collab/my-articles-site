from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, SubscriberViewSet, PhotoViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'subscribers', SubscriberViewSet)
router.register(r'photos', PhotoViewSet)

urlpatterns = router.urls