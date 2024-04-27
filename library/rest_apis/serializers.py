from rest_framework import serializers
from library.models import (
    Book, Author, BookAuthorMapper, Member, BookMemberMapper
)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Retrieve the authors associated with the book
        authors = Author.objects.filter(bookauthormapper__book=instance)
        # Serialize the authors
        author_serializer = AuthorSerializer(authors, many=True)
        representation['authors'] = author_serializer.data
        
        # Issued book
        issued = len(BookMemberMapper.objects.filter(book=instance.id, book_status="issued"))
        representation['issued'] = issued
        
        # Instock book
        representation['in_stock'] = instance.quantity - issued
        return representation


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookAuthorMapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAuthorMapper
        fields = "__all__"
        
        
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"
        
    # Custom field level validation
    def validate_member_code(self, value):
        if value is not None:
            if (len(value) != 5):
                raise serializers.ValidationError("Library Code must be 5 characters.")
            if not (value[0] == "L" and value[1] == "M"):
                raise serializers.ValidationError("First character should be 'L' and second should be 'M'.")
            if not (value[2:].isnumeric()):
                raise serializers.ValidationError("Third, fourth and fifth characters must be numbers.")
        return value
    
    
class BookMemberMapperSerilizer(serializers.ModelSerializer):
    class Meta:
        model = BookMemberMapper
        fields= "__all__"