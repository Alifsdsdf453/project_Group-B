from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, UserProfileView, 
    BookListCreateView, BookDetailView,
    BorrowBookView, MyBorrowingsView, ReturnBookView
)

urlpatterns = [
    
    path('api/register/', RegisterView.as_view(), name='register'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/profile/', UserProfileView.as_view(), name='profile'),

    path('api/books/', BookListCreateView.as_view(), name='book-list'),

    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    path('api/borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('api/my-borrows/', MyBorrowingsView.as_view(), name='my-borrows'),

    path('api/return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
]