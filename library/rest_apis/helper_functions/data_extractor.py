from library.rest_apis.serializers import (
    BookSerializer, AuthorSerializer, BookAuthorMapperSerializer
)


def book(title=None, copyright=None):
    _book = {
        "title": title,
        "copyright": copyright
    }
    return _book


def author(name=None, birth_year=None, death_year=None):
    _author = {
        "name": name,
        "birth_year": birth_year,
        "death_year": death_year
    }
    return _author


def data_extractor_guten_dex(data_list):
    for data in data_list:        
        _book = book(title=data["title"], copyright=data["copyright"])
        book_serializer = BookSerializer(data=_book)
        if book_serializer.is_valid():
            book_serializer.save()
        else:
            pass
        author_serializer = AuthorSerializer(data=data["authors"], many=True)
        if author_serializer.is_valid():
            author_serializer.save()
        else:
            pass
    return None