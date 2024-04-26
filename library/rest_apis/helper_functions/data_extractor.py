from library.rest_apis.serializers import (
    BookSerializer, AuthorSerializer, BookAuthorMapperSerializer
)

from library.models import Book


def redundent_data_remover(data_list):
    """
    Remove redundant data from a list of dictionaries based on unique titles.

    Args:
        data_list (list): A list of dictionaries representing data items.

    Returns:
        list: A list of dictionaries with unique titles.
    """
    
    # Use a set to keep track of unique titles
    unique_titles = set()
    
    # List to store dictionaries with unique titles
    unique_data = []
    
    # Iterate over the dataset
    for book in data_list:
        title = book["title"]
        # Check if the title is already in the set
        if title not in unique_titles:
            # If not, add it to the set and append the dictionary to the unique_data list
            unique_titles.add(title)
            unique_data.append(book)
    
    return unique_data


def book(title=None, copyright=None, quantity=None):
    """
    Helper function to create a dictionary representing a book.

    Args:
        title (str): The title of the book.
        copyright (bool): The copyright status of the book.
        quantity (int): The quantity of the book.

    Returns:
        dict: A dictionary representing a book.
    """
    _book = {
        "title": title,
        "copyright": copyright,
        "quantity": quantity
    }
    return _book


def author(name=None, birth_year=None, death_year=None):
    """
    Helper function to create a dictionary representing an author.

    Args:
        name (str): The name of the author.
        birth_year (int): The birth year of the author.
        death_year (int): The death year of the author.

    Returns:
        dict: A dictionary representing an author.
    """
    _author = {
        "name": name,
        "birth_year": birth_year,
        "death_year": death_year
    }
    return _author


def data_extractor_guten_dex(data_list, quantity=None):
    """
    Extract data from a list of dictionaries and save it into the database.

    Args:
        data_list (list): A list of dictionaries representing data items.
        quantity (int, optional): The quantity to increment (if applicable).

    Returns:
        None
    """
    
    # to remove duplicate data from data_list
    unique_data_list = redundent_data_remover(data_list)
    
    for data in unique_data_list:
        try:
            # if book exist, then only increment the quantity if quantity is given
            existing_book = Book.objects.get(title=data["title"])
            existing_book.quantity = existing_book.quantity + quantity
            existing_book.save()
        except:
            if quantity:
                _book = book(title=data["title"], copyright=data["copyright"], quantity=quantity)
            else:
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