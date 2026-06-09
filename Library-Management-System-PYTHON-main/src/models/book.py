
class Book:
    """Represents a book in the library."""
    
    def __init__(self, book_id, title, author, category, quantity):
        """
        Initialize a Book instance.
        
        Args:
            book_id (int): Unique identifier for the book
            title (str): Title of the book
            author (str): Author of the book
            category (str): Category of the book
            quantity (int): Total quantity in library
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity
    
    def __repr__(self):
        return f"Book(id={self.book_id}, title='{self.title}', author='{self.author}', qty={self.quantity})"
    
    def to_dict(self):
        """Convert book to dictionary."""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'quantity': self.quantity
        }
