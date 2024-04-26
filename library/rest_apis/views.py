import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .helper_functions.url_creators import url_creator
from .helper_functions.data_extractor import data_extractor_guten_dex
from .helper_functions.context_generator import context_data_generator


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