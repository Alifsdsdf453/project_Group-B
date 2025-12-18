from rest_framework import serializers
from .models import Author,Book,BorrowingRecord
from django.contrib.auth.models import User
import os
MAX_SIZE=2*1024*1024
SAVE_EXTS={'jpg','jpeg','png'}
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','username']

class ProfileSerializer(serializers.ModelSerializer):
      class Meta:
         model = User
         fields = ['id', 'username', 'email']
         read_only_fields = ['id', 'username']
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=['id','name','bio']
class BookSerializer(serializers.ModelSerializer):
    author=AuthorSerializer(many=True,read_only=True)
    class Meta:
        model=Book
        fields=['id','title','author','isbn','year_publication','genre','copies_total','copies_available','image_cover']
        read_only_fields=['author','copies_available']
    def validate_image_cover(self,image):
        if image.size>MAX_SIZE:
           raise serializers.ValidationError('image too big')
        ext=os.path.splitext(image.name)[1]
        if ext not in SAVE_EXTS:
            raise serializers.ValidationError('image extension not supported')
        if not image.content_type.startswith('image/'):
            raise serializers.ValidationError('file not image')
        return image
class BorrowingRecordSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    book=BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True,
        source='book'
    )
    class Meta:
        model=BorrowingRecord
        fields=['id','user','book','book_id','date_borrow','date_due','date_return','returned_is']
        read_only_fields=['user','book','date_borrow','date_due','date_return','returned_is']
