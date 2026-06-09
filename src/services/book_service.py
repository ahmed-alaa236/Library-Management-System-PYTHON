
from src.models.book import Book
from src.utils.validation import Validator

class BookService:
    """Service class for book-related operations."""
    
    def __init__(self, db):
        """
        Initialize BookService.
        
        Args:
            db: Database connection object
        """
        self.db = db
        self.validator = Validator()
    
    def add_book(self, title, author, category, quantity):
        """
        Add a new book to the library.
        
        Args:
            title (str): Book title
            author (str): Author name
            category (str): Book category
            quantity (int): Number of copies
            
        Returns:
            int: ID of the newly added book
        """
        # Validation
        if not self.validator.validate_string(title, min_length=1):
            raise ValueError("Title cannot be empty")
        if not self.validator.validate_string(author, min_length=1):
            raise ValueError("Author cannot be empty")
        if not self.validator.validate_non_negative_int(quantity):
            raise ValueError("Quantity must be >= 0")
        
        query = """
            INSERT INTO books (title, author, category, quantity)
            VALUES (?, ?, ?, ?)
        """
        book_id = self.db.execute_insert(query, (title, author, category, quantity))
        print(f"✓ Book added successfully with ID: {book_id}")
        return book_id
    
    def get_book_by_id(self, book_id):
        """
        Retrieve a book by ID.
        
        Args:
            book_id (int): Book ID
            
        Returns:
            Book: Book object or None if not found
        """
        query = "SELECT * FROM books WHERE book_id = ?"
        result = self.db.execute(query, (book_id,))
        if result:
            row = result[0]
            return Book(row['book_id'], row['title'], row['author'], 
                       row['category'], row['quantity'])
        return None
    
    def get_all_books(self):
        """
        Retrieve all books from the library.
        
        Returns:
            list: List of Book objects
        """
        query = "SELECT * FROM books ORDER BY title"
        results = self.db.execute(query)
        books = []
        for row in results:
            books.append(Book(row['book_id'], row['title'], row['author'],
                            row['category'], row['quantity']))
        return books
    
    def search_by_title(self, title):
        """
        Search for books by title.
        
        Args:
            title (str): Book title to search
            
        Returns:
            list: List of matching Book objects
        """
        query = "SELECT * FROM books WHERE title LIKE ? ORDER BY title"
        results = self.db.execute(query, (f'%{title}%',))
        books = []
        for row in results:
            books.append(Book(row['book_id'], row['title'], row['author'],
                            row['category'], row['quantity']))
        return books
    
    def search_by_author(self, author):
        """
        Search for books by author.
        
        Args:
            author (str): Author name to search
            
        Returns:
            list: List of matching Book objects
        """
        query = "SELECT * FROM books WHERE author LIKE ? ORDER BY author"
        results = self.db.execute(query, (f'%{author}%',))
        books = []
        for row in results:
            books.append(Book(row['book_id'], row['title'], row['author'],
                            row['category'], row['quantity']))
        return books
    
    def update_book(self, book_id, title=None, author=None, category=None, quantity=None):
        """
        Update book information.
        
        Args:
            book_id (int): Book ID
            title (str): New title (optional)
            author (str): New author (optional)
            category (str): New category (optional)
            quantity (int): New quantity (optional)
            
        Returns:
            bool: True if updated successfully
        """
        updates = []
        params = []
        
        if title is not None:
            if not self.validator.validate_string(title, min_length=1):
                raise ValueError("Title cannot be empty")
            updates.append("title = ?")
            params.append(title)
        if author is not None:
            if not self.validator.validate_string(author, min_length=1):
                raise ValueError("Author cannot be empty")
            updates.append("author = ?")
            params.append(author)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if quantity is not None:
            if not self.validator.validate_non_negative_int(quantity):
                raise ValueError("Quantity must be >= 0")
            updates.append("quantity = ?")
            params.append(quantity)
        
        if not updates:
            return False
        
        params.append(book_id)
        query = f"UPDATE books SET {', '.join(updates)} WHERE book_id = ?"
        
        affected = self.db.execute_update(query, tuple(params))
        if affected > 0:
            print(f"✓ Book {book_id} updated successfully")
            return True
        return False
    
    def delete_book(self, book_id):
        """
        Delete a book from the library.
        
        Args:
            book_id (int): Book ID
            
        Returns:
            bool: True if deleted successfully
        """
        query = "DELETE FROM books WHERE book_id = ?"
        affected = self.db.execute_delete(query, (book_id,))
        if affected > 0:
            print(f"✓ Book {book_id} deleted successfully")
            return True
        print(f"✗ Book {book_id} not found")
        return False
