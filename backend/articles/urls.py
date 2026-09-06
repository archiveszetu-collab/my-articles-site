from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, SubscriberViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'subscribers', SubscriberViewSet)

urlpatterns = router.urls