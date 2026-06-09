
class Reports:
    """Generate reports using SQL aggregate functions."""
    
    def __init__(self, db):
        """
        Initialize Reports.
        
        Args:
            db: Database connection object
        """
        self.db = db
    
    def total_books_count(self):
        """
        Get total count of books in library.
        
        Returns:
            int: Total number of books
        """
        query = "SELECT COUNT(*) as total FROM books"
        result = self.db.execute(query)
        return result[0]['total'] if result else 0
    
    def total_members_count(self):
        """
        Get total count of members.
        
        Returns:
            int: Total number of members
        """
        query = "SELECT COUNT(*) as total FROM members"
        result = self.db.execute(query)
        return result[0]['total'] if result else 0
    
    def active_loans_count(self):
        """
        Get count of active loans (not returned).
        
        Returns:
            int: Total number of active loans
        """
        query = "SELECT COUNT(*) as total FROM loans WHERE return_date IS NULL"
        result = self.db.execute(query)
        return result[0]['total'] if result else 0
    
    def most_borrowed_books(self, limit=5):
        """
        Get most borrowed books using GROUP BY.
        
        Args:
            limit (int): Number of top books to return
            
        Returns:
            list: List of book records with borrow count
        """
        query = """
            SELECT 
                b.book_id,
                b.title,
                b.author,
                COUNT(l.loan_id) as borrow_count
            FROM books b
            LEFT JOIN loans l ON b.book_id = l.book_id
            GROUP BY b.book_id, b.title, b.author
            ORDER BY borrow_count DESC
            LIMIT ?
        """
        return self.db.execute(query, (limit,))
    
    def available_books(self):
        """
        Get count of available books (quantity > 0).
        
        Returns:
            int: Total number of available books
        """
        query = "SELECT COUNT(*) as total FROM books WHERE quantity > 0"
        result = self.db.execute(query)
        return result[0]['total'] if result else 0
    
    def unavailable_books(self):
        """
        Get count of unavailable books (quantity = 0).
        
        Returns:
            int: Total number of unavailable books
        """
        query = "SELECT COUNT(*) as total FROM books WHERE quantity = 0"
        result = self.db.execute(query)
        return result[0]['total'] if result else 0
    
    def books_by_category(self):
        """
        Get count of books by category.
        
        Returns:
            list: List of categories with book count
        """
        query = """
            SELECT 
                category,
                COUNT(*) as count
            FROM books
            GROUP BY category
            ORDER BY count DESC
        """
        return self.db.execute(query)
    
    def member_loan_history(self, member_id):
        """
        Get loan history for a specific member.
        
        Args:
            member_id (int): Member ID
            
        Returns:
            list: List of loans for the member
        """
        query = """
            SELECT 
                l.loan_id,
                b.title,
                b.author,
                l.borrow_date,
                l.return_date
            FROM loans l
            JOIN books b ON l.book_id = b.book_id
            WHERE l.member_id = ?
            ORDER BY l.borrow_date DESC
        """
        return self.db.execute(query, (member_id,))
    
    def top_members(self, limit=5):
        """
        Get top borrowers (members with most loans).
        
        Args:
            limit (int): Number of top members to return
            
        Returns:
            list: List of members with loan count
        """
        query = """
            SELECT 
                m.member_id,
                m.full_name,
                m.email,
                COUNT(l.loan_id) as total_loans
            FROM members m
            LEFT JOIN loans l ON m.member_id = l.member_id
            GROUP BY m.member_id, m.full_name, m.email
            ORDER BY total_loans DESC
            LIMIT ?
        """
        return self.db.execute(query, (limit,))
    
    def total_quantity_in_library(self):
        """
        Get total quantity of all books in library.
        
        Returns:
            int: Total quantity
        """
        query = "SELECT SUM(quantity) as total FROM books"
        result = self.db.execute(query)
        return result[0]['total'] if result and result[0]['total'] else 0
    
    def print_summary_report(self):
        """Print a formatted summary report."""
        print("\n" + "=" * 60)
        print("LIBRARY MANAGEMENT SYSTEM - SUMMARY REPORT")
        print("=" * 60)
        
        print(f"\n📚 Total Books: {self.total_books_count()}")
        print(f"👥 Total Members: {self.total_members_count()}")
        print(f"📤 Active Loans: {self.active_loans_count()}")
        print(f"✓ Available Books: {self.available_books()}")
        print(f"✗ Unavailable Books: {self.unavailable_books()}")
        print(f"📦 Total Quantity in Library: {self.total_quantity_in_library()}")
        
        print("\n" + "-" * 60)
        print("TOP 5 MOST BORROWED BOOKS:")
        print("-" * 60)
        
        most_borrowed = self.most_borrowed_books(5)
        if most_borrowed:
            for i, book in enumerate(most_borrowed, 1):
                print(f"{i}. {book['title']} by {book['author']} - Borrowed {book['borrow_count']} times")
        else:
            print("No books borrowed yet")
        
        print("\n" + "-" * 60)
        print("TOP 5 MEMBERS:")
        print("-" * 60)
        
        top_members = self.top_members(5)
        if top_members:
            for i, member in enumerate(top_members, 1):
                print(f"{i}. {member['full_name']} ({member['email']}) - {member['total_loans']} loans")
        else:
            print("No members registered yet")
        
        print("\n" + "-" * 60)
        print("BOOKS BY CATEGORY:")
        print("-" * 60)
        
        by_category = self.books_by_category()
        if by_category:
            for cat in by_category:
                category = cat['category'] if cat['category'] else "No Category"
                print(f"  {category}: {cat['count']} books")
        else:
            print("No books registered yet")
        
        print("\n" + "=" * 60 + "\n")
