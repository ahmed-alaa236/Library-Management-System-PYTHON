-- Sample Data for Library Management System

-- Insert Sample Books
INSERT INTO books (title, author, category, quantity) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 3),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 2),
('1984', 'George Orwell', 'Dystopian', 4),
('Pride and Prejudice', 'Jane Austen', 'Romance', 2),
('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 3),
('Python Programming', 'Guido van Rossum', 'Technology', 5),
('Introduction to Algorithms', 'Thomas H. Cormen', 'Technology', 4),
('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 3),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 'Fantasy', 6),
('Atomic Habits', 'James Clear', 'Self-Help', 5);

-- Insert Sample Members
INSERT INTO members (full_name, email, phone) VALUES
('Alice Johnson', 'alice.johnson@email.com', '555-0101'),
('Bob Smith', 'bob.smith@email.com', '555-0102'),
('Carol Williams', 'carol.williams@email.com', '555-0103'),
('David Brown', 'david.brown@email.com', '555-0104'),
('Emily Davis', 'emily.davis@email.com', '555-0105'),
('Frank Miller', 'frank.miller@email.com', '555-0106'),
('Grace Lee', 'grace.lee@email.com', '555-0107'),
('Henry Wilson', 'henry.wilson@email.com', '555-0108');

-- Insert Sample Loans (some active, some returned)
INSERT INTO loans (book_id, member_id, borrow_date, return_date) VALUES
(1, 1, '2024-01-01', '2024-01-15'),
(2, 2, '2024-01-05', '2024-01-20'),
(3, 3, '2024-01-10', NULL),
(4, 1, '2024-01-12', NULL),
(5, 2, '2024-01-15', '2024-01-30'),
(6, 4, '2024-01-18', NULL),
(7, 5, '2024-01-20', '2024-02-05'),
(8, 3, '2024-01-22', NULL),
(9, 6, '2024-01-25', NULL),
(10, 7, '2024-01-28', NULL),
(1, 2, '2024-02-01', NULL),
(3, 4, '2024-02-02', NULL);
