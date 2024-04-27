from django.urls import path
from .views import (
    GetBooks, BookList, BookDetail, MemberList, MemberDetail, BookMemberMapperList
)

urlpatterns = [
    # To books in the library
    path('get_books/', GetBooks.as_view(), name='get_books'),
    
    path('book_list/', BookList.as_view(), name='book_list'),
    path('book_detail/<int:id>/', BookDetail.as_view(), name='book_detail'),
    
    path('member_list/', MemberList.as_view(), name='member_list'),
    path('member_detail/<int:id>/', MemberDetail.as_view(), name='member_detail'),
    
    path('book_member_mapper/', BookMemberMapperList.as_view(), name='book_member_mapper'),
]