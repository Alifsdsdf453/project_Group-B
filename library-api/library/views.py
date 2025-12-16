from .serializers import BookSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Book

class BookPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            return request.method in permissions.SAFE_METHODS
        return False

class BooksViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [BookPermissions]
