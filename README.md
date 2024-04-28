# Drivex Test Assignment Django REST Framework: Library Management System

## Table of Contents

- introduction
- features
- installation
- usage

## Introduction

Library Management Web Application

A local library is in dire need of a web application to ease their work. The library management system must allow a librarian to track books and their quantity, books issued to members, book fees.

For the sake of simplicity, app will be used by the librarian only.

The following functionalities are expected from the application:

Base Library System

# Librarians must be able to maintain:
-	Books with stock maintained
-	Members
-	Transactions

# The use cases included here are to:
-	Perform general CRUD operations on Books and Members
-	Issue a book to a member
-	Issue a book return from a member
-	Search for a book by name and author
-	Charge a rent fee on book returns
-	Make sure a member’s outstanding debt is not more than Rs.500

## Installation
- Clone the repository to your local machine using Git:
    git clone https://github.com/mayankbth/drivex_test_assignment_django.git

- Navigate to the project directory and install the required dependencies using pip:
    cd <project_directory>
    pip install -r requirements.txt

- Apply migrations to create database tables:
    python manage.py migrate

- Create a Superuser (Optional)
    python manage.py createsuperuser

- Run the Development Server
    python manage.py runserver

- Access the Application
    http://127.0.0.1:8000/


# Usage
# APIs 
- http://127.0.0.1:8000/library/get_books/
- http://127.0.0.1:8000/library/book_list/
- http://127.0.0.1:8000/library/book_detail/<int:id>/
- http://127.0.0.1:8000/library/member_list/
- http://127.0.0.1:8000/library/member_detail/<int:id>/
- http://127.0.0.1:8000/library/book_member_mapper/
- http://127.0.0.1:8000/library/book_member_mapper/<int:id>/

## Explanation

## http://127.0.0.1:8000/library/get_books/
- **Methods:** GET, POST
- **API Endpoint:** `/books/`
  - **GET:** Retrieve book data based on provided query parameters.
  - **POST:** Process and save book data obtained from an external API.
- **Query Parameters:** 
  - `page`: Pagination parameter to specify the page number.
  - `search`: Search parameter to filter books based on specific criteria.
- **Payload Example:**
  ```json
  {
    "quantity": 10
  }
- If the payload is provided in the POST request, the specified quantity will be assigned to the book or books becoming available in the library.
