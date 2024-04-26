from rest_framework import serializers
from library.models import (
    Book, Author, BookAuthorMapper
)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookAuthorMapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthorMapper
        fields = "__all__"