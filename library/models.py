from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=200, unique=True)
    copyright = models.BooleanField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    rent_fee = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
class Authors(models.Model):
    name = models.CharField(max_length=200, unique=True)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class BooksAuthorsMappers(models.Model):
    books = models.ForeignKey(Books, on_delete=models.CASCADE)
    authors = models.ForeignKey(Authors, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.books + "|" + self.authors