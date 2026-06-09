from src.db import Database
from src.services.book_service import BookService
from src.services.member_service import MemberService
from src.services.loan_service import LoanService

print("Starting simple tests...")

db = Database("test_library.db")
db.connect()
db.init_db()

book_service = BookService(db)
member_service = MemberService(db)
loan_service = LoanService(db)

# Add book
book_id = book_service.add_book(
    "Python Basics",
    "Ahmed Ali",
    "Programming",
    5
)

# Add member
member_id = member_service.add_member(
    "Mohamed Hassan",
    "mohamed@gmail.com",
    "01012345678"
)

# Borrow book
loan_id = loan_service.borrow_book(
    book_id,
    member_id
)

print("Book added successfully")
print("Member added successfully")
print("Loan created successfully")
print("All tests passed")

db.disconnect()