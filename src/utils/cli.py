"""CLI Interface for Library Management System."""

import sys
from datetime import datetime

class CLI:
    """Command Line Interface for the Library Management System."""
    
    def __init__(self, book_service, member_service, loan_service, reports):
        """
        Initialize CLI with services.
        
        Args:
            book_service: BookService instance
            member_service: MemberService instance
            loan_service: LoanService instance
            reports: Reports instance
        """
        self.book_service = book_service
        self.member_service = member_service
        self.loan_service = loan_service
        self.reports = reports
    
    def print_header(self, title):
        """Print a formatted header."""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def print_menu(self, options):
        """Print menu options."""
        for key, value in options.items():
            print(f"{key}. {value}")
        print()
    
    def get_input(self, prompt, input_type=str):
        """
        Get validated user input.
        
        Args:
            prompt: Input prompt
            input_type: Type to convert input to
            
        Returns:
            User input converted to specified type
        """
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("✗ Input cannot be empty. Please try again.")
                    continue
                if input_type == int:
                    return int(user_input)
                return user_input
            except ValueError:
                print(f"✗ Invalid input. Please enter a valid {input_type.__name__}.")
            except KeyboardInterrupt:
                print("\n✗ Exiting...")
                sys.exit(0)
    
    def display_table(self, headers, rows):
        """Display data in table format."""
        if not rows:
            print("✗ No records found")
            return
        
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Print header
        header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        print(header_row)
        print("-" * len(header_row))
        
        # Print rows
        for row in rows:
            print(" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
    
    # ============= MAIN MENU =============
    def main_menu(self):
        """Display main menu."""
        while True:
            self.print_header("LIBRARY MANAGEMENT SYSTEM")
            options = {
                "1": "Books Management",
                "2": "Members Management",
                "3": "Loans Management",
                "4": "Reports",
                "5": "Exit"
            }
            self.print_menu(options)
            
            choice = self.get_input("Select an option: ")
            
            if choice == "1":
                self.books_menu()
            elif choice == "2":
                self.members_menu()
            elif choice == "3":
                self.loans_menu()
            elif choice == "4":
                self.reports_menu()
            elif choice == "5":
                print("\n✓ Thank you for using Library Management System!")
                sys.exit(0)
            else:
                print("✗ Invalid option. Please try again.")
    
    # ============= BOOKS MENU =============
    def books_menu(self):
        """Display books menu."""
        while True:
            self.print_header("BOOKS MANAGEMENT")
            options = {
                "1": "Add Book",
                "2": "Show All Books",
                "3": "Search Book by ID",
                "4": "Search Book by Title",
                "5": "Search Book by Author",
                "6": "Update Book",
                "7": "Delete Book",
                "8": "Back to Main Menu"
            }
            self.print_menu(options)
            
            choice = self.get_input("Select an option: ")
            
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.show_books()
            elif choice == "3":
                self.search_book_by_id()
            elif choice == "4":
                self.search_book_by_title()
            elif choice == "5":
                self.search_book_by_author()
            elif choice == "6":
                self.update_book()
            elif choice == "7":
                self.delete_book()
            elif choice == "8":
                return
            else:
                print("✗ Invalid option. Please try again.")
    
    def add_book(self):
        """Add a new book."""
        self.print_header("ADD NEW BOOK")
        try:
            title = self.get_input("Book Title: ")
            author = self.get_input("Author: ")
            category = self.get_input("Category: ")
            quantity = self.get_input("Quantity: ", int)
            
            self.book_service.add_book(title, author, category, quantity)
            print("✓ Book added successfully!")
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        input("\nPress Enter to continue...")
    
    def show_books(self):
        """Display all books."""
        self.print_header("ALL BOOKS")
        try:
            books = self.book_service.get_all_books()
            if books:
                headers = ["ID", "Title", "Author", "Category", "Quantity"]
                rows = [[b.book_id, b.title, b.author, b.category, b.quantity] for b in books]
                self.display_table(headers, rows)
                print(f"\nTotal books: {len(books)}")
            else:
                print("✗ No books found")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def search_book_by_id(self):
        """Search for a book by ID."""
        self.print_header("SEARCH BOOK BY ID")
        try:
            book_id = self.get_input("Enter Book ID: ", int)
            book = self.book_service.get_book_by_id(book_id)
            if book:
                headers = ["ID", "Title", "Author", "Category", "Quantity"]
                rows = [[book.book_id, book.title, book.author, book.category, book.quantity]]
                self.display_table(headers, rows)
            else:
                print(f"✗ Book with ID {book_id} not found")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def search_book_by_title(self):
        """Search for books by title."""
        self.print_header("SEARCH BOOKS BY TITLE")
        try:
            title = self.get_input("Enter Title (or part of title): ")
            books = self.book_service.search_by_title(title)
            if books:
                headers = ["ID", "Title", "Author", "Category", "Quantity"]
                rows = [[b.book_id, b.title, b.author, b.category, b.quantity] for b in books]
                self.display_table(headers, rows)
                print(f"\nFound {len(books)} book(s)")
            else:
                print(f"✗ No books found with title containing '{title}'")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def search_book_by_author(self):
        """Search for books by author."""
        self.print_header("SEARCH BOOKS BY AUTHOR")
        try:
            author = self.get_input("Enter Author Name (or part of name): ")
            books = self.book_service.search_by_author(author)
            if books:
                headers = ["ID", "Title", "Author", "Category", "Quantity"]
                rows = [[b.book_id, b.title, b.author, b.category, b.quantity] for b in books]
                self.display_table(headers, rows)
                print(f"\nFound {len(books)} book(s)")
            else:
                print(f"✗ No books found by author '{author}'")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def update_book(self):
        """Update book information."""
        self.print_header("UPDATE BOOK")
        try:
            book_id = self.get_input("Enter Book ID to update: ", int)
            book = self.book_service.get_book_by_id(book_id)
            if not book:
                print(f"✗ Book with ID {book_id} not found")
                input("\nPress Enter to continue...")
                return
            
            print(f"\nCurrent info: {book.title} by {book.author}")
            print("(Leave blank to keep current value)\n")
            
            title = self.get_input("New Title (or press Enter to skip): ") or None
            author = self.get_input("New Author (or press Enter to skip): ") or None
            category = self.get_input("New Category (or press Enter to skip): ") or None
            quantity_input = self.get_input("New Quantity (or press Enter to skip): ") or None
            quantity = int(quantity_input) if quantity_input else None
            
            if self.book_service.update_book(book_id, title, author, category, quantity):
                print("✓ Book updated successfully!")
            else:
                print("✗ No changes made")
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        input("\nPress Enter to continue...")
    
    def delete_book(self):
        """Delete a book."""
        self.print_header("DELETE BOOK")
        try:
            book_id = self.get_input("Enter Book ID to delete: ", int)
            book = self.book_service.get_book_by_id(book_id)
            if not book:
                print(f"✗ Book with ID {book_id} not found")
                input("\nPress Enter to continue...")
                return
            
            print(f"\nBook: {book.title} by {book.author}")
            confirm = self.get_input("Are you sure you want to delete this book? (yes/no): ").lower()
            
            if confirm == "yes":
                if self.book_service.delete_book(book_id):
                    print("✓ Book deleted successfully!")
                else:
                    print("✗ Failed to delete book")
            else:
                print("✗ Deletion cancelled")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    # ============= MEMBERS MENU =============
    def members_menu(self):
        """Display members menu."""
        while True:
            self.print_header("MEMBERS MANAGEMENT")
            options = {
                "1": "Add Member",
                "2": "Show All Members",
                "3": "Search Member by ID",
                "4": "Search Member by Name",
                "5": "Search Member by Email",
                "6": "Update Member",
                "7": "Delete Member",
                "8": "Back to Main Menu"
            }
            self.print_menu(options)
            
            choice = self.get_input("Select an option: ")
            
            if choice == "1":
                self.add_member()
            elif choice == "2":
                self.show_members()
            elif choice == "3":
                self.search_member_by_id()
            elif choice == "4":
                self.search_member_by_name()
            elif choice == "5":
                self.search_member_by_email()
            elif choice == "6":
                self.update_member()
            elif choice == "7":
                self.delete_member()
            elif choice == "8":
                return
            else:
                print("✗ Invalid option. Please try again.")
    
    def add_member(self):
        """Add a new member."""
        self.print_header("ADD NEW MEMBER")
        try:
            full_name = self.get_input("Full Name: ")
            email = self.get_input("Email: ")
            phone = self.get_input("Phone: ")
            
            self.member_service.add_member(full_name, email, phone)
            print("✓ Member added successfully!")
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        input("\nPress Enter to continue...")
    
    def show_members(self):
        """Display all members."""
        self.print_header("ALL MEMBERS")
        try:
            members = self.member_service.get_all_members()
            if members:
                headers = ["ID", "Full Name", "Email", "Phone"]
                rows = [[m.member_id, m.full_name, m.email, m.phone] for m in members]
                self.display_table(headers, rows)
                print(f"\nTotal members: {len(members)}")
            else:
                print("✗ No members found")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def search_member_by_id(self):
        """Search for a member by ID."""
        self.print_header("SEARCH MEMBER BY ID")
        try:
            member_id = self.get_input("Enter Member ID: ", int)
            member = self.member_service.get_member_by_id(member_id)
            if member:
                headers = ["ID", "Full Name", "Email", "Phone"]
                rows = [[member.member_id, member.full_name, member.email, member.phone]]
                self.display_table(headers, rows)
            else:
                print(f"✗ Member with ID {member_id} not found")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def search_member_by_name(self):
        """Search for members by name."""
        self.print_header("SEARCH MEMBERS BY NAME")
        try:
            name = self.get_input("Enter Name (or part of name): ")
            members = self.member_service.search_by_name(name)
            if members:
                headers = ["ID", "Full Name", "Email", "Phone"]
                rows = [[m.member_id, m.full_name, m.email, m.phone] for m in members]
                self.display_table(headers, rows)
                print(f"\nFound {len(members)} member(s)")
            else:
                print(f"✗ No members found with name containing '{name}'")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def search_member_by_email(self):
        """Search for members by email."""
        self.print_header("SEARCH MEMBERS BY EMAIL")
        try:
            email = self.get_input("Enter Email (or part of email): ")
            members = self.member_service.search_by_email(email)
            if members:
                headers = ["ID", "Full Name", "Email", "Phone"]
                rows = [[m.member_id, m.full_name, m.email, m.phone] for m in members]
                self.display_table(headers, rows)
                print(f"\nFound {len(members)} member(s)")
            else:
                print(f"✗ No members found with email containing '{email}'")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def update_member(self):
        """Update member information."""
        self.print_header("UPDATE MEMBER")
        try:
            member_id = self.get_input("Enter Member ID to update: ", int)
            member = self.member_service.get_member_by_id(member_id)
            if not member:
                print(f"✗ Member with ID {member_id} not found")
                input("\nPress Enter to continue...")
                return
            
            print(f"\nCurrent info: {member.full_name} ({member.email})")
            print("(Leave blank to keep current value)\n")
            
            full_name = self.get_input("New Full Name (or press Enter to skip): ") or None
            email = self.get_input("New Email (or press Enter to skip): ") or None
            phone = self.get_input("New Phone (or press Enter to skip): ") or None
            
            if self.member_service.update_member(member_id, full_name, email, phone):
                print("✓ Member updated successfully!")
            else:
                print("✗ No changes made")
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        input("\nPress Enter to continue...")
    
    def delete_member(self):
        """Delete a member."""
        self.print_header("DELETE MEMBER")
        try:
            member_id = self.get_input("Enter Member ID to delete: ", int)
            member = self.member_service.get_member_by_id(member_id)
            if not member:
                print(f"✗ Member with ID {member_id} not found")
                input("\nPress Enter to continue...")
                return
            
            print(f"\nMember: {member.full_name} ({member.email})")
            confirm = self.get_input("Are you sure you want to delete this member? (yes/no): ").lower()
            
            if confirm == "yes":
                if self.member_service.delete_member(member_id):
                    print("✓ Member deleted successfully!")
                else:
                    print("✗ Failed to delete member")
            else:
                print("✗ Deletion cancelled")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    # ============= LOANS MENU =============
    def loans_menu(self):
        """Display loans menu."""
        while True:
            self.print_header("LOANS MANAGEMENT")
            options = {
                "1": "Borrow Book",
                "2": "Return Book",
                "3": "Show All Loans",
                "4": "Show Active Loans",
                "5": "Member Loan History",
                "6": "Back to Main Menu"
            }
            self.print_menu(options)
            
            choice = self.get_input("Select an option: ")
            
            if choice == "1":
                self.borrow_book()
            elif choice == "2":
                self.return_book()
            elif choice == "3":
                self.show_all_loans()
            elif choice == "4":
                self.show_active_loans()
            elif choice == "5":
                self.member_loan_history()
            elif choice == "6":
                return
            else:
                print("✗ Invalid option. Please try again.")
    
    def borrow_book(self):
        """Borrow a book."""
        self.print_header("BORROW BOOK")
        try:
            member_id = self.get_input("Enter Member ID: ", int)
            book_id = self.get_input("Enter Book ID: ", int)
            
            # Verify member and book exist
            member = self.member_service.get_member_by_id(member_id)
            if not member:
                print(f"✗ Member with ID {member_id} not found")
                input("\nPress Enter to continue...")
                return
            
            book = self.book_service.get_book_by_id(book_id)
            if not book:
                print(f"✗ Book with ID {book_id} not found")
                input("\nPress Enter to continue...")
                return
            
            print(f"\nMember: {member.full_name}")
            print(f"Book: {book.title}")
            print(f"Available: {book.quantity}")
            
            if book.quantity <= 0:
                print("✗ This book is not available")
                input("\nPress Enter to continue...")
                return
            
            confirm = self.get_input("Confirm borrow? (yes/no): ").lower()
            if confirm == "yes":
                loan_id = self.loan_service.borrow_book(book_id, member_id)
                print(f"✓ Book borrowed successfully! Loan ID: {loan_id}")
            else:
                print("✗ Borrow cancelled")
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        input("\nPress Enter to continue...")
    
    def return_book(self):
        """Return a borrowed book."""
        self.print_header("RETURN BOOK")
        try:
            loan_id = self.get_input("Enter Loan ID: ", int)
            loan = self.loan_service.get_loan_by_id(loan_id)
            
            if not loan:
                print(f"✗ Loan with ID {loan_id} not found")
                input("\nPress Enter to continue...")
                return
            
            if not loan.is_active():
                print("✗ This book has already been returned")
                input("\nPress Enter to continue...")
                return
            
            book = self.book_service.get_book_by_id(loan.book_id)
            member = self.member_service.get_member_by_id(loan.member_id)
            
            print(f"\nMember: {member.full_name}")
            print(f"Book: {book.title}")
            print(f"Borrow Date: {loan.borrow_date}")
            
            confirm = self.get_input("Confirm return? (yes/no): ").lower()
            if confirm == "yes":
                self.loan_service.return_book(loan_id)
                print("✓ Book returned successfully!")
            else:
                print("✗ Return cancelled")
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        input("\nPress Enter to continue...")
    
    def show_all_loans(self):
        """Display all loans."""
        self.print_header("ALL LOANS")
        try:
            loans = self.loan_service.get_all_loans()
            if loans:
                headers = ["Loan ID", "Member Name", "Book Title", "Borrow Date", "Return Date"]
                rows = [
                    [l['loan_id'], l['full_name'], l['title'], l['borrow_date'], 
                     l['return_date'] if l['return_date'] else "Not Returned"]
                    for l in loans
                ]
                self.display_table(headers, rows)
                print(f"\nTotal loans: {len(loans)}")
            else:
                print("✗ No loans found")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def show_active_loans(self):
        """Display active loans."""
        self.print_header("ACTIVE LOANS")
        try:
            loans = self.loan_service.get_active_loans()
            if loans:
                headers = ["Loan ID", "Member Name", "Book Title", "Borrow Date"]
                rows = [
                    [l['loan_id'], l['full_name'], l['title'], l['borrow_date']]
                    for l in loans
                ]
                self.display_table(headers, rows)
                print(f"\nTotal active loans: {len(loans)}")
            else:
                print("✗ No active loans")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def member_loan_history(self):
        """Display member loan history."""
        self.print_header("MEMBER LOAN HISTORY")
        try:
            member_id = self.get_input("Enter Member ID: ", int)
            member = self.member_service.get_member_by_id(member_id)
            
            if not member:
                print(f"✗ Member with ID {member_id} not found")
                input("\nPress Enter to continue...")
                return
            
            print(f"\nMember: {member.full_name}\n")
            
            loans = self.reports.member_loan_history(member_id)
            if loans:
                headers = ["Loan ID", "Book Title", "Author", "Borrow Date", "Return Date"]
                rows = [
                    [l['loan_id'], l['title'], l['author'], l['borrow_date'],
                     l['return_date'] if l['return_date'] else "Not Returned"]
                    for l in loans
                ]
                self.display_table(headers, rows)
                print(f"\nTotal loans: {len(loans)}")
            else:
                print("✗ No loans found for this member")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    # ============= REPORTS MENU =============
    def reports_menu(self):
        """Display reports menu."""
        while True:
            self.print_header("REPORTS")
            options = {
                "1": "Summary Report",
                "2": "Most Borrowed Books",
                "3": "Top Members",
                "4": "Books by Category",
                "5": "Back to Main Menu"
            }
            self.print_menu(options)
            
            choice = self.get_input("Select an option: ")
            
            if choice == "1":
                self.reports.print_summary_report()
                input("Press Enter to continue...")
            elif choice == "2":
                self.show_most_borrowed()
            elif choice == "3":
                self.show_top_members()
            elif choice == "4":
                self.show_books_by_category()
            elif choice == "5":
                return
            else:
                print("✗ Invalid option. Please try again.")
    
    def show_most_borrowed(self):
        """Display most borrowed books."""
        self.print_header("MOST BORROWED BOOKS")
        try:
            books = self.reports.most_borrowed_books(10)
            if books:
                headers = ["Book ID", "Title", "Author", "Times Borrowed"]
                rows = [[b['book_id'], b['title'], b['author'], b['borrow_count']] for b in books]
                self.display_table(headers, rows)
            else:
                print("✗ No books found")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def show_top_members(self):
        """Display top members."""
        self.print_header("TOP MEMBERS")
        try:
            members = self.reports.top_members(10)
            if members:
                headers = ["Member ID", "Name", "Email", "Total Loans"]
                rows = [[m['member_id'], m['full_name'], m['email'], m['total_loans']] for m in members]
                self.display_table(headers, rows)
            else:
                print("✗ No members found")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
    
    def show_books_by_category(self):
        """Display books by category."""
        self.print_header("BOOKS BY CATEGORY")
        try:
            categories = self.reports.books_by_category()
            if categories:
                headers = ["Category", "Count"]
                rows = [[c['category'] if c['category'] else "No Category", c['count']] for c in categories]
                self.display_table(headers, rows)
            else:
                print("✗ No categories found")
        except Exception as e:
            print(f"✗ Error: {e}")
        input("\nPress Enter to continue...")
