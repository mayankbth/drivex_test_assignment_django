from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    copyright = models.BooleanField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    rent_fee = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class BookAuthorMapper(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)