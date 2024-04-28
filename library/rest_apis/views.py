import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .helper_functions.url_creators import url_creator
from .helper_functions.data_extractor import data_extractor_guten_dex
from .helper_functions.context_generator import context_data_generator

from .serializers import *

from library.models import Book, Member, BookMemberMapper


class GetBooks(APIView):
    """
    API endpoint to retrieve and process book data.

    Methods:
        - get: Retrieve book data based on provided query parameters.
        - post: Process and save book data obtained from an external API.
    """
    
    def get(self, request):
        """
        Retrieve book data based on provided query parameters.

        Args:
            request (HttpRequest): HTTP request object.

        Returns:
            Response: Response object containing book data.
        """
        
        page = request.GET.get('page')
        search = request.GET.get('search')
        
        url = url_creator(page, search)
        
        try:
            response = requests.get(url)
            context = context_data_generator(
                info= "Success",
                status_code= status.HTTP_200_OK,
                data= response.json()
            )
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            context = context_data_generator(
                info= "Fail",
                status_code= status.HTTP_400_BAD_REQUEST,
                error_message= str(e)
            )
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request):
        """
        Process and save book data obtained from an external API.

        Args:
            request (HttpRequest): HTTP request object.

        Returns:
            Response: Response object indicating success or failure.
        """
        
        page = request.GET.get('page')
        search = request.GET.get('search')
        
        url = url_creator(page, search)
        
        try:
            response = requests.get(url)
        except Exception as e:
            context = context_data_generator(
                info= "Fail",
                status_code= status.HTTP_400_BAD_REQUEST,
                error_message= str(e)
            )
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data_list = response.json()["results"]
        except Exception as e:
            context = context_data_generator(
                info= "Fail",
                status_code= status.HTTP_400_BAD_REQUEST,
                error_message= "No result found"
            )
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quantity = request.data["quantity"]
            data_extractor_guten_dex(data_list, quantity=quantity)
        except:
            data_extractor_guten_dex(data_list)

        context = context_data_generator(
            info= "Success",
            status_code= status.HTTP_200_OK,
            data= data_list
        )
        return Response(context, status=status.HTTP_200_OK)
    
    
class BookList(APIView):
    """
    A view to retrieve a list of books based on provided query parameters.

    If both 'book_title' and 'author_name' are provided, it filters books by
    title and author name. If only 'author_name' is provided, it filters books
    by author name. If only 'book_title' is provided, it filters books by title.
    If no query parameters are provided, it returns all books.

    Returns:
        Response: A response containing a list of serialized books.
    """
    def get(self, request):
        
        book_title = request.GET.get('book_title')
        author_name = request.GET.get('author_name')
        
        if (book_title and author_name):
            
            # Define the Q objects
            q_title = Q(title__icontains=book_title)
            q_author = Q(bookauthormapper__author__name__icontains=author_name)
            
            # Combine the Q objects using logical OR operator
            q_combined = q_title & q_author
            
            # query_set = Book.objects.filter(title=book_title, bookauthormapper__author__name=author_name)
            query_set = Book.objects.filter(q_combined)
            
        elif author_name:
            query_set = Book.objects.filter(bookauthormapper__author__name__icontains=author_name)
        elif book_title:
            query_set = Book.objects.filter(title__icontains=book_title)
        else:
            query_set = Book.objects.all()
            
        serializer = BookSerializer(query_set, many=True)
        
        context = context_data_generator(
            info= "Success",
            status_code= status.HTTP_200_OK,
            data= serializer.data
        )
        return Response(context, status=status.HTTP_200_OK)
    
    
class BookDetail(APIView):
    """
    A view to retrieve, update, or partially update details of a specific book.

    GET:
    Retrieve details of a book with the specified ID.

    PATCH:
    Update or partially update details of a book with the specified ID.
    If 'quantity' is provided in the request data, it adds the new quantity to the existing quantity.
    If the resulting quantity is negative, returns a Bad Request response.

    Args:
        request: The HTTP request object.
        id: The ID of the book to retrieve or update.

    Returns:
        Response: A response containing information about the success or failure of the operation,
        along with the data of the book if successful.
    """
    
    def get(self, request, id):
        
        try:
            book = Book.objects.get(id=id)
        except:
            context = context_data_generator(
                info= "Fail",
                status_code= status.HTTP_404_NOT_FOUND,
            )
            return Response(context, status.HTTP_404_NOT_FOUND)
        
        serializer = BookSerializer(book)
        
        context = context_data_generator(
            info= "Success",
            status_code= status.HTTP_200_OK,
            data= serializer.data
        )
        
        return Response(context, status=status.HTTP_200_OK)
        
        
    def patch(self, request, id):
        
        try:
            book = Book.objects.get(id=id)
        except:
            context = context_data_generator(
                info= "Fail",
                status_code= status.HTTP_404_NOT_FOUND,
            )
            return Response(context, status.HTTP_404_NOT_FOUND)
        
        try:
            # if 'quantity' is present in validated_data, add the new quantity to the existing quantity
            request.data["quantity"] = book.quantity + request.data["quantity"]
            if request.data["quantity"] < 0:
                context = context_data_generator(
                    info="Fail",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error_message="Book quantity can not be negative."
                )
                return Response(context, status.HTTP_400_BAD_REQUEST)
        except:
            pass
        
        serializer = BookSerializer(book, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            context = context_data_generator(
                info="Success",
                status_code=status.HTTP_200_OK,
                data=serializer.data
            )
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_message=serializer.errors
            )
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        
class MemberList(APIView):
    """
    A view to retrieve a list of all members or add a new member.

    GET:
    Retrieve a list of all members.

    POST:
    Add a new member to the system.

    Args:
        request: The HTTP request object.

    Returns:
        Response: A response containing information about the success or failure of the operation,
        along with the data of all members if retrieving or the data of the added member if creating.
    """
    
    def get(self, request):
        
        member = Member.objects.all()
        serializer = MemberSerializer(member, many=True)
        context = context_data_generator(
            info="Success",
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )
        return Response(context, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = context_data_generator(
                info="Success",
                status_code=status.HTTP_201_CREATED,
                data=serializer.data
            )
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_message=serializer.errors
            )
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        
class MemberDetail(APIView):
    """
    A view to retrieve, update, or delete details of a specific member.

    GET:
    Retrieve details of a member with the specified ID.

    PATCH:
    Update details of a member with the specified ID.
    If 'partial' is True, only provided fields in the request data will be updated.

    DELETE:
    Delete a member with the specified ID.

    Args:
        request: The HTTP request object.
        id: The ID of the member to retrieve, update, or delete.

    Returns:
        Response: A response containing information about the success or failure of the operation,
        along with the data of the member if retrieving or updating.
    """
    def get(self, request, id):
        
        try:
            member = Member.objects.get(id=id)
        except Member.DoesNotExist:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_404_NOT_FOUND,
                error_message=f"Member with ID {id} does not exist."
            )
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MemberSerializer(member)
        context = context_data_generator(
            info=f"Success",
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )
        return Response(context, status=status.HTTP_200_OK)
    
    
    def patch(self, request, id):
        
        try:
            member = Member.objects.get(id=id)
        except Member.DoesNotExist:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_404_NOT_FOUND,
                error_message=f"Member with ID {id} does not exist."
            )
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MemberSerializer(member, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            context = context_data_generator(
                info="Success",
                status_code=status.HTTP_200_OK,
                data=serializer.data
            )
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_message=serializer.errors
            )
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, id):

        try:
            member = Member.objects.get(id=id)
        except Member.DoesNotExist:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_404_NOT_FOUND,
                error_message=f"Member with ID {id} does not exist."
            )
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        member.delete()
        context = context_data_generator(
            info="Success",
            status_code=status.HTTP_204_NO_CONTENT
        )
        return Response(context, status=status.HTTP_204_NO_CONTENT)
    
    
class BookMemberMapperList(APIView):
    """
    A view to retrieve a list of all book-member mappings or add a new mapping.

    GET:
    Retrieve a list of all book-member mappings.

    POST:
    Add a new book-member mapping to the system.

    Args:
        request: The HTTP request object.

    Returns:
        Response: A response containing information about the success or failure of the operation,
        along with the data of all book-member mappings if retrieving or the data of the added mapping if creating.
    """
    def get(self, request):
        
        mapper_object = BookMemberMapper.objects.all()
        serializer = BookMemberMapperSerilizer(mapper_object, many=True)
        context = context_data_generator(
            info="Success",
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )
        return Response(context, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        
        serializer = BookMemberMapperSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = context_data_generator(
                info="Success",
                status_code=status.HTTP_201_CREATED,
                data=serializer.data
            )
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_message=serializer.errors
            )
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        
class BookMemberMapperDetail(APIView):
    """
    A view to retrieve, update, or delete a specific book-member mapping.

    GET:
    Retrieve details of a book-member mapping with the specified ID.

    PATCH:
    Update details of a book-member mapping with the specified ID.

    DELETE:
    Delete a book-member mapping with the specified ID.

    Args:
        request: The HTTP request object.
        id: The ID of the book-member mapping to retrieve, update, or delete.

    Returns:
        Response: A response containing information about the success or failure of the operation,
        along with the data of the book-member mapping if retrieving or updating.
    """
    
    def get(self, request, id):
        
        try:
            book_member = BookMemberMapper.objects.get(id=id)
        except BookMemberMapper.DoesNotExist:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_404_NOT_FOUND,
                error_message=f"BookMemberMapper with ID {id} does not exist."
            )
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookMemberMapperSerilizer(book_member)
        context = context_data_generator(
            info=f"Success",
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )
        return Response(context, status=status.HTTP_200_OK)


    def patch(self, request, id):
        
        try:
            book_member = BookMemberMapper.objects.get(id=id)
        except BookMemberMapper.DoesNotExist:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_404_NOT_FOUND,
                error_message=f"BookMemberMapper with ID {id} does not exist."
            )
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookMemberMapperSerilizer(book_member, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            context = context_data_generator(
                info="Success",
                status_code=status.HTTP_200_OK,
                data=serializer.data
            )
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_400_BAD_REQUEST,
                error_message=serializer.errors
            )
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, id):

        try:
            book_member = BookMemberMapper.objects.get(id=id)
        except BookMemberMapper.DoesNotExist:
            context = context_data_generator(
                info="Fail",
                status_code=status.HTTP_404_NOT_FOUND,
                error_message=f"BookMemberMapper with ID {id} does not exist."
            )
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        
        book_member.delete()
        context = context_data_generator(
            info="Success",
            status_code=status.HTTP_204_NO_CONTENT
        )
        return Response(context, status=status.HTTP_204_NO_CONTENT)