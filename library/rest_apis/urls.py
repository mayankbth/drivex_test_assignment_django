from django.urls import path
from .views import (
    GetBooks, BookList, BookDetail, MemberList
)

urlpatterns = [
    # To books in the library
    path('get_books/', GetBooks.as_view(), name='get_books'),
    
    path('book_list/', BookList.as_view(), name='book_list'),
    path('book_detail/<int:id>/', BookDetail.as_view(), name='book_detail'),
    
    path('member_list/', MemberList.as_view(), name='member_list'),
]