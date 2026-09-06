from rest_framework.permissions import BasePermission
from django.conf import settings

class HasUploadKey(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        key = request.headers.get('X-Upload-Key')
        return key == settings.ARTICLE_UPLOAD_KEY