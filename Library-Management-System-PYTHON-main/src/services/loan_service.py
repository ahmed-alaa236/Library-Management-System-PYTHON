
from datetime import datetime
from src.models.loan import Loan

class LoanService:
    """Service class for loan-related operations."""
    
    def __init__(self, db):
        """
        Initialize LoanService.
        
        Args:
            db: Database connection object
        """
        self.db = db
    
    def borrow_book(self, book_id, member_id, borrow_date=None):
        """
        Borrow a book for a member.
        
        Steps:
        1. Verify member exists
        2. Verify book exists
        3. Verify quantity > 0
        4. Create loan record
        5. Reduce book quantity by 1
        
        Args:
            book_id (int): Book ID
            member_id (int): Member ID
            borrow_date (str): Borrow date (default: today, format YYYY-MM-DD)
            
        Returns:
            int: ID of the newly created loan
        """
        if borrow_date is None:
            borrow_date = datetime.now().strftime('%Y-%m-%d')
        
        # Verify member exists
        member_check = self.db.execute(
            "SELECT member_id FROM members WHERE member_id = ?", 
            (member_id,)
        )
        if not member_check:
            raise ValueError(f"Member ID {member_id} not found")
        
        # Verify book exists and check quantity
        book_check = self.db.execute(
            "SELECT quantity FROM books WHERE book_id = ?", 
            (book_id,)
        )
        if not book_check:
            raise ValueError(f"Book ID {book_id} not found")
        
        if book_check[0]['quantity'] <= 0:
            raise ValueError("Book is not available")
        
        try:
            # Create loan record
            loan_query = """
                INSERT INTO loans (book_id, member_id, borrow_date, return_date)
                VALUES (?, ?, ?, NULL)
            """
            loan_id = self.db.execute_insert(loan_query, (book_id, member_id, borrow_date))
            
            # Reduce book quantity
            update_query = "UPDATE books SET quantity = quantity - 1 WHERE book_id = ?"
            self.db.execute_update(update_query, (book_id,))
            
            print(f"✓ Book borrowed successfully. Loan ID: {loan_id}")
            return loan_id
        except Exception as e:
            print(f"✗ Error creating loan: {e}")
            raise
    
    def return_book(self, loan_id, return_date=None):
        """
        Return a borrowed book.
        
        Steps:
        1. Select loan
        2. Update return_date
        3. Increase quantity by 1
        
        Args:
            loan_id (int): Loan ID
            return_date (str): Return date (default: today, format YYYY-MM-DD)
            
        Returns:
            bool: True if return processed successfully
        """
        if return_date is None:
            return_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Get loan details
            loan_check = self.db.execute(
                "SELECT * FROM loans WHERE loan_id = ? AND return_date IS NULL",
                (loan_id,)
            )
            if not loan_check:
                raise ValueError("Loan not found or already returned")
            
            loan_row = loan_check[0]
            book_id = loan_row['book_id']
            
            # Update loan with return date
            update_loan = "UPDATE loans SET return_date = ? WHERE loan_id = ?"
            self.db.execute_update(update_loan, (return_date, loan_id))
            
            # Increase book quantity
            update_book = "UPDATE books SET quantity = quantity + 1 WHERE book_id = ?"
            self.db.execute_update(update_book, (book_id,))
            
            print(f"✓ Book returned successfully")
            return True
        except Exception as e:
            print(f"✗ Error returning book: {e}")
            raise
    
    def get_loan_by_id(self, loan_id):
        """
        Retrieve a loan by ID.
        
        Args:
            loan_id (int): Loan ID
            
        Returns:
            Loan: Loan object or None if not found
        """
        query = "SELECT * FROM loans WHERE loan_id = ?"
        result = self.db.execute(query, (loan_id,))
        if result:
            row = result[0]
            return Loan(row['loan_id'], row['book_id'], row['member_id'],
                       row['borrow_date'], row['return_date'])
        return None
    
    def get_all_loans(self):
        """
        Retrieve all loans with member and book details using JOIN.
        
        Returns:
            list: List of loan details with member and book info
        """
        query = """
            SELECT 
                l.loan_id,
                l.book_id,
                l.member_id,
                l.borrow_date,
                l.return_date,
                m.full_name,
                b.title
            FROM loans l
            JOIN members m ON l.member_id = m.member_id
            JOIN books b ON l.book_id = b.book_id
            ORDER BY l.borrow_date DESC
        """
        return self.db.execute(query)
    
    def get_active_loans(self):
        """
        Retrieve all active loans (not returned).
        
        Returns:
            list: List of active loan details with member and book info
        """
        query = """
            SELECT 
                l.loan_id,
                l.book_id,
                l.member_id,
                l.borrow_date,
                l.return_date,
                m.full_name,
                b.title
            FROM loans l
            JOIN members m ON l.member_id = m.member_id
            JOIN books b ON l.book_id = b.book_id
            WHERE l.return_date IS NULL
            ORDER BY l.borrow_date DESC
        """
        return self.db.execute(query)
    
    def get_member_loans(self, member_id):
        """
        Retrieve all loans for a specific member.
        
        Args:
            member_id (int): Member ID
            
        Returns:
            list: List of Loan objects
        """
        query = "SELECT * FROM loans WHERE member_id = ? ORDER BY borrow_date DESC"
        results = self.db.execute(query, (member_id,))
        loans = []
        for row in results:
            loans.append(Loan(row['loan_id'], row['book_id'], row['member_id'],
                            row['borrow_date'], row['return_date']))
        return loans
    
    def get_book_loans(self, book_id):
        """
        Retrieve all loans for a specific book.
        
        Args:
            book_id (int): Book ID
            
        Returns:
            list: List of Loan objects
        """
        query = "SELECT * FROM loans WHERE book_id = ? ORDER BY borrow_date DESC"
        results = self.db.execute(query, (book_id,))
        loans = []
        for row in results:
            loans.append(Loan(row['loan_id'], row['book_id'], row['member_id'],
                            row['borrow_date'], row['return_date']))
        return loans
