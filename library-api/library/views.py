from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Book, Author, BorrowingRecord
from .serializers import (BookSerializer, AuthorSerializer, BorrowingRecordSerializer, UserSerializer, ProfileSerializer)

class BookPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [BookPermissions]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class BorrowingViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowingRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BorrowingRecord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        if book.copies_available > 0:
            instance = serializer.save(user=self.request.user)
            instance.borrow_book()
        else:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("عذراً، لا توجد نسخ متاحة حالياً لهذا الكتاب.")

class ReturnBookView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request, pk):
        try:
            record = BorrowingRecord.objects.get(pk=pk)
            self.check_object_permissions(request, record)
            
            if record.returned_is:
                return Response({"detail": "تم إرجاع الكتاب سابقاً."}, status=status.HTTP_400_BAD_REQUEST)
            record.return_book()
            return Response({"message": "تم إرجاع الكتاب بنجاح وتحديث المخزن."}, status=status.HTTP_200_OK)
            
        except BorrowingRecord.DoesNotExist:
            return Response({"detail": "سجل الإعارة غير موجود."}, status=status.HTTP_404_NOT_FOUND)




