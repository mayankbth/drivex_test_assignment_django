from django.urls import path
from .views import (
    GetBooks
)

urlpatterns = [
    path('get_books/', GetBooks.as_view(), name='get_books'),
]