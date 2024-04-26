import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .helper_functions.url_creators import url_creator
from .helper_functions.data_extractor import data_extractor_guten_dex
from .helper_functions.context_generator import context_data_generator

from .serializers import *

from library.models import Book


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
            query_set = Book.objects.filter(title=book_title, bookauthormapper__author__name=author_name)
        elif author_name:
            query_set = Book.objects.filter(bookauthormapper__author__name=author_name)
        elif book_title:
            query_set = Book.objects.filter(title=book_title)
        else:
            query_set = Book.objects.all()
            
        serializer = BookSerializer(query_set, many=True)
        
        context = context_data_generator(
            info= "Success",
            status_code= status.HTTP_200_OK,
            data= serializer.data
        )
        return Response(context, status=status.HTTP_200_OK)