from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'copyright', 'quantity', 'rent_fee')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_year', 'death_year')


class BookAuthorMapperAdmin(admin.ModelAdmin):
    list_display = ('book', 'author')
    
    
class MemberAdmin(admin.ModelAdmin):
    list_display = ('member_code', 'name')
    
    
class BookMemberMapperAdmin(admin.ModelAdmin):
    list_display = ('book', 'member')


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthorMapper, BookAuthorMapperAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(BookMemberMapper, BookMemberMapperAdmin)