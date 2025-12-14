from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Book, BorrowingRecord
from .serializers import UserSerializer, BookSerializer, BorrowingRecordSerializer
from .permissions import IsOwner

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class BorrowBookView(generics.CreateAPIView):
    serializer_class = BorrowingRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        instance.borrow_book()

class MyBorrowingsView(generics.ListAPIView):
    serializer_class = BorrowingRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BorrowingRecord.objects.filter(user=self.request.user)

class ReturnBookView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request, pk):
        try:
            record = BorrowingRecord.objects.get(pk=pk)
            self.check_object_permissions(request, record)
            if record.returned_is:
                return Response({"error": "the book is returned already"}, status=status.HTTP_400_BAD_REQUEST)
            
            record.return_book() 
            return Response({"message": "the book has been returned successfully"}, status=status.HTTP_200_OK)
        except BorrowingRecord.DoesNotExist:
            return Response({"error": "the record is not exist"}, status=status.HTTP_404_NOT_FOUND)