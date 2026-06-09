
from src.db import Database
from src.services.book_service import BookService
from src.services.member_service import MemberService
from src.services.loan_service import LoanService
from src.utils.reports import Reports
from src.utils.cli import CLI

def main():
    """Main function to run the library management system."""
    try:
        # Initialize database
        db = Database('database/library.db')
        db.connect()
        db.init_db()
        
        # Initialize services
        book_service = BookService(db)
        member_service = MemberService(db)
        loan_service = LoanService(db)
        reports = Reports(db)
        
        # Initialize CLI and run
        cli = CLI(book_service, member_service, loan_service, reports)
        cli.main_menu()
        
    except KeyboardInterrupt:
        print("\n✗ Interrupted by user")
    except Exception as e:
        print(f"✗ Fatal error: {e}")
    finally:
        if 'db' in locals():
            db.disconnect()

if __name__ == "__main__":
    main()
