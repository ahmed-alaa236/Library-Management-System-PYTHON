SELECT * FROM books;

SELECT * FROM members;

SELECT * FROM loans;

SELECT
    l.loan_id,
    b.title,
    m.full_name,
    l.borrow_date,
    l.return_date
FROM loans l
JOIN books b ON l.book_id = b.book_id
JOIN members m ON l.member_id = m.member_id;

SELECT
    b.title,
    COUNT(l.loan_id) AS borrow_count
FROM books b
LEFT JOIN loans l
ON b.book_id = l.book_id
GROUP BY b.title
ORDER BY borrow_count DESC;