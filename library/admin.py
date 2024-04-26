from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'copyright', 'quantity', 'rent_fee')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_year', 'death_year')


class BookAuthorMapperAdmin(admin.ModelAdmin):
    list_display = ('book', 'author')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthorMapper, BookAuthorMapperAdmin)