# Library Management System

## Project Overview

This project is a simple Library Management System developed using Python and SQLite for the WAP 228 Workplace Application course.

The system allows users to manage books, members, and borrowing records through a Command Line Interface (CLI).

## Technologies Used

* Python
* SQLite
* GitHub

## Database Tables

### Books

* book_id
* title
* author
* category
* quantity

### Members

* member_id
* full_name
* email
* phone

### Loans

* loan_id
* book_id
* member_id
* borrow_date
* return_date

## Features

### Book Management

* Add Book
* View Books
* Update Book
* Delete Book

### Member Management

* Add Member
* View Members
* Update Member
* Delete Member

### Loan Management

* Borrow Book
* Return Book
* View Loans

## Project Structure

```text
database/
src/
tests/
README.md
requirements.txt
```

## How to Run

```bash
python -m src.main
```

## Testing

A simple test file was created to verify:

* Database connection
* Add Book
* Add Member
* Borrow Book

Run:

```bash
python -m tests.test_system
```

## Sample SQL Queries

### Show All Books

```sql
SELECT * FROM books;
```

### Show All Members

```sql
SELECT * FROM members;
```

### Active Loans

```sql
SELECT *
FROM loans
WHERE return_date IS NULL;
```

### Most Borrowed Books

```sql
SELECT book_id, COUNT(*) AS borrow_count
FROM loans
GROUP BY book_id
ORDER BY borrow_count DESC;
```

## What I Learned

### Python

* Working with functions and classes
* Using SQLite with Python
* Building a CLI application

### SQL

* Creating tables
* CRUD operations
* Using JOIN and GROUP BY

### GitHub

* Creating repositories
* Uploading projects
* Using commits

## Conclusion

This project helped me understand how Python and SQL can work together to build a simple database application.
