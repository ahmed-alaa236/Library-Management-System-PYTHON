
import sqlite3
from pathlib import Path

class Database:
    """Handles database operations for the library system."""
    
    def __init__(self, db_path='database/library.db'):
        """
        Initialize database connection.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self._ensure_db_dir()
    
    def _ensure_db_dir(self):
        """Ensure database directory exists."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def connect(self):
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            # Enable foreign keys
            self.connection.execute("PRAGMA foreign_keys = ON")
            print(f"✓ Connected to database: {self.db_path}")
            return self.connection
        except sqlite3.Error as e:
            print(f"✗ Database connection error: {e}")
            raise
    
    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            print("✓ Disconnected from database")
    
    def execute(self, query, params=None):
        """
        Execute a SELECT query.
        
        Args:
            query (str): SQL query
            params (tuple): Query parameters
            
        Returns:
            list: Query results
        """
        if not self.connection:
            raise RuntimeError("Database not connected")
        
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Query execution error: {e}")
            raise
    
    def execute_insert(self, query, params=None):
        """
        Execute an INSERT query.
        
        Args:
            query (str): SQL INSERT query
            params (tuple): Query parameters
            
        Returns:
            int: ID of inserted row
        """
        if not self.connection:
            raise RuntimeError("Database not connected")
        
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"✗ Insert error: {e}")
            raise
    
    def execute_update(self, query, params=None):
        """
        Execute an UPDATE query.
        
        Args:
            query (str): SQL UPDATE query
            params (tuple): Query parameters
            
        Returns:
            int: Number of affected rows
        """
        if not self.connection:
            raise RuntimeError("Database not connected")
        
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"✗ Update error: {e}")
            raise
    
    def execute_delete(self, query, params=None):
        """
        Execute a DELETE query.
        
        Args:
            query (str): SQL DELETE query
            params (tuple): Query parameters
            
        Returns:
            int: Number of deleted rows
        """
        if not self.connection:
            raise RuntimeError("Database not connected")
        
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"✗ Delete error: {e}")
            raise
    
    def init_db(self):
        """Initialize database with required tables."""
        try:
            # Create books table
            self.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    category TEXT,
                    quantity INTEGER NOT NULL CHECK(quantity >= 0)
                )
            """)
            
            # Create members table
            self.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT
                )
            """)
            
            # Create loans table
            self.execute("""
                CREATE TABLE IF NOT EXISTS loans (
                    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    member_id INTEGER NOT NULL,
                    borrow_date DATE NOT NULL,
                    return_date DATE,
                    FOREIGN KEY(book_id) REFERENCES books(book_id),
                    FOREIGN KEY(member_id) REFERENCES members(member_id)
                )
            """)
            
            print("✓ Database tables initialized successfully")
        except sqlite3.Error as e:
            print(f"✗ Database initialization error: {e}")
            raise
