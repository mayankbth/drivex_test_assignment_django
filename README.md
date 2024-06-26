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
- **API Endpoint:** `/get_books/`
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

## http://127.0.0.1:8000/library/book_list/
- **Methods:** GET
- **API Endpoint:** `/book_list/`
    - **GET:** Retrieve available books in library, based on provided query parameters.
- **Query Parameters:** 
  - `book_title`: search based on book_title.
  - `author_name`: search based on author_name.
- **Payload Example:** None

## http://127.0.0.1:8000/library/book_detail/<int:id>/
- **Methods:** GET, PATCH
- **API Endpoint:** `/book_detail/<int:id>/`, (Obtain the ID from the "http://127.0.0.1:8000/library/book_list/" endpoint using the GET method)
    - **GET:** Retrieve available book in the library based on the provided ID.
    - **PATCH:** Update related data for an available book in the library based on the provided ID and payload.
- **Query Parameters:**: none
- **Payload Example:**
  ```json
  {
    "quantity": 10
  }
- If the above payload is provided, it will increase the quantity of the book with the given ID by 10.

## http://127.0.0.1:8000/library/member_list/
- **Methods:** GET, POST
- **API Endpoint:** `/member_list/`
    - **GET:** Retrive all the members created in the system.
    - **POST:** TO create new members.
- **Query Parameters:**: none
- **Payload Example:**
  ```json
  {
    "name": "mayank2",
    "member_code": "LM002"
  }
- This payload will create a new member with "name: mayank2" and "member_code: LM002".

## http://127.0.0.1:8000/library/member_detail/<int:id>/
- **Methods:** GET, PATCH, DELETE
- **API Endpoint:** `/member_detail/<int:id>/`, (Obtain the ID from the "http://127.0.0.1:8000/library/member_list/" endpoint using the GET method)
    - **GET:** Retrieve member based on the provided ID.
    - **PATCH:** To perform update operation on members based on provided ID and payload.
    - **DELETE:** To delete a member based on the provided ID.
- **Query Parameters:**: none
- **Payload Example:**
  ```json
  {
    "name": "mayank111",
    "member_code": "LM111"
  }
- This payload will update the "name" and "member_code" of the member.

## http://127.0.0.1:8000/library/book_member_mapper/
- **Methods:** GET, POST
- **API Endpoint:** `/book_member_mapper/`
    - **GET:** Retrive all the transction data from "Book member mappers" (Transction data related to books and members)
    - **POST:** TO create a new transaction.
- **Query Parameters:**: none
- **Payload Example:**
  ```json
  {
    "book": 12,
    "member": 2,
    "book_status": "issued",
    "fee_status": "pending"
  }
- This payload will create a new transction between "book_id: 12" and "member_id: 2".

## http://127.0.0.1:8000/library/book_member_mapper/<int:id>/
- **Methods:** GET, PATCH, DELETE
- **API Endpoint:** `/book_member_mapper/<int:id>/`, (Obtain the ID from the "http://127.0.0.1:8000/library/book_member_mapper/" endpoint using the GET method)
    - **GET:** Retrieve transction data based on the provided ID.
    - **PATCH:** To perform update operation on members based on provided ID and payload.
    - **DELETE:** To delete a member based on the provided ID.
- **Query Parameters:**: none
- **Payload Example:**
  ```json
  {
    "book_status": "returned",
    "fee_status": "paid"
  }
- This payload will update the "book_status" and "fee_status" of the Transction from "issued - returned" and "pending - paid" and other way arround.