from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Book, BorrowingRecord

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['copies_available']

class BorrowingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingRecord
        fields = '__all__'
        read_only_fields = ['user', 'date_borrow', 'date_due', 'date_return', 'returned_is']

    def validate_book(self, value):
        if value.copies_available <= 0:
            raise serializers.ValidationError("its not available")
        return value