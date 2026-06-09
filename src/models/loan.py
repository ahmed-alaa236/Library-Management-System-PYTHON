

from datetime import datetime

class Loan:
    """Represents a book loan transaction."""
    
    def __init__(self, loan_id, book_id, member_id, borrow_date, return_date=None):
        """
        Initialize a Loan instance.
        
        Args:
            loan_id (int): Unique identifier for the loan
            book_id (int): ID of the loaned book
            member_id (int): ID of the member who loaned the book
            borrow_date (str): Date of borrow (YYYY-MM-DD)
            return_date (str): Date of return, None if not yet returned
        """
        self.loan_id = loan_id
        self.book_id = book_id
        self.member_id = member_id
        self.borrow_date = borrow_date
        self.return_date = return_date
    
    def is_active(self):
        """Check if the loan is still active (not returned)."""
        return self.return_date is None
    
    def __repr__(self):
        status = "Returned" if self.return_date else "Active"
        return f"Loan(id={self.loan_id}, book={self.book_id}, member={self.member_id}, status={status})"
    
    def to_dict(self):
        """Convert loan to dictionary."""
        return {
            'loan_id': self.loan_id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'borrow_date': self.borrow_date,
            'return_date': self.return_date
        }
