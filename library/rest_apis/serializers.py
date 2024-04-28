from rest_framework import serializers
from library.models import (
    Book, Author, BookAuthorMapper, Member, BookMemberMapper
)

from .helper_functions.enums import max_pending_balance as mpb


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
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation["book_title"] = str(instance.book)
        representation["member_code"] = str(instance.member)
        
        return representation
    
    def validate_book_status(self, value):
        
        if value == "issued":
            
            # getting the number of books issued form BookMemberMapper
            issued_book = len(BookMemberMapper.objects.filter(book=self.initial_data["book"], book_status=value))
            # getting in stock books by substracting the issued_books form the total quantity
            book_instance = Book.objects.get(id=self.initial_data["book"])
            in_stock_book = book_instance.quantity - issued_book
            
            # if book is not in stock and being assign then raise error
            if not in_stock_book:
                raise serializers.ValidationError(f"{book_instance.title} is not in stock.")
            
            # if the book is already assigned to a perticular member then raise error
            member_instance = Member.objects.get(id=self.initial_data["member"])
            if BookMemberMapper.objects.filter(book=book_instance.id, member=member_instance.id, book_status="issued"):
                raise serializers.ValidationError(f"{book_instance.title} book has been already issued to {member_instance.member_code}.")
            
            # TO denied the issue of book if balance ammount is more than 500 for a member.
            if (len(BookMemberMapper.objects.filter(member=member_instance.id, fee_status="pending"))*(book_instance.rent_fee)==mpb):
                raise serializers.ValidationError(f"{member_instance.member_code} has reached maximum allowed balance.")
            
        return value