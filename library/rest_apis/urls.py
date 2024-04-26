from django.urls import path
from .views import (
    GetBooks, BookList
)

urlpatterns = [
    # To books in the library
    path('get_books/', GetBooks.as_view(), name='get_books'),
    
    path('book_list/', BookList.as_view(), name='book_list'),
]