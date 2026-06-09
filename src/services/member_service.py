
from src.models.member import Member
from src.utils.validation import Validator

class MemberService:
    """Service class for member-related operations."""
    
    def __init__(self, db):
        """
        Initialize MemberService.
        
        Args:
            db: Database connection object
        """
        self.db = db
        self.validator = Validator()
    
    def add_member(self, full_name, email, phone):
        """
        Add a new member to the library.
        
        Args:
            full_name (str): Member full name
            email (str): Email address
            phone (str): Phone number
            
        Returns:
            int: ID of the newly added member
        """
        # Validation
        if not self.validator.validate_string(full_name, min_length=1):
            raise ValueError("Full name is required")
        if not self.validator.validate_email(email):
            raise ValueError("Invalid email format")
        
        try:
            query = """
                INSERT INTO members (full_name, email, phone)
                VALUES (?, ?, ?)
            """
            member_id = self.db.execute_insert(query, (full_name, email, phone))
            print(f"✓ Member added successfully with ID: {member_id}")
            return member_id
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Email '{email}' is already registered")
            raise
    
    def get_member_by_id(self, member_id):
        """
        Retrieve a member by ID.
        
        Args:
            member_id (int): Member ID
            
        Returns:
            Member: Member object or None if not found
        """
        query = "SELECT * FROM members WHERE member_id = ?"
        result = self.db.execute(query, (member_id,))
        if result:
            row = result[0]
            return Member(row['member_id'], row['full_name'], row['email'],
                         row['phone'])
        return None
    
    def get_all_members(self):
        """
        Retrieve all members.
        
        Returns:
            list: List of Member objects
        """
        query = "SELECT * FROM members ORDER BY full_name"
        results = self.db.execute(query)
        members = []
        for row in results:
            members.append(Member(row['member_id'], row['full_name'], row['email'],
                                 row['phone']))
        return members
    
    def search_by_name(self, full_name):
        """
        Search for members by name.
        
        Args:
            full_name (str): Name to search
            
        Returns:
            list: List of matching Member objects
        """
        query = "SELECT * FROM members WHERE full_name LIKE ? ORDER BY full_name"
        results = self.db.execute(query, (f'%{full_name}%',))
        members = []
        for row in results:
            members.append(Member(row['member_id'], row['full_name'], row['email'],
                                 row['phone']))
        return members
    
    def search_by_email(self, email):
        """
        Search for members by email.
        
        Args:
            email (str): Email to search
            
        Returns:
            list: List of matching Member objects
        """
        query = "SELECT * FROM members WHERE email LIKE ?"
        results = self.db.execute(query, (f'%{email}%',))
        members = []
        for row in results:
            members.append(Member(row['member_id'], row['full_name'], row['email'],
                                 row['phone']))
        return members
    
    def update_member(self, member_id, full_name=None, email=None, phone=None):
        """
        Update member information.
        
        Args:
            member_id (int): Member ID
            full_name (str): New name (optional)
            email (str): New email (optional)
            phone (str): New phone (optional)
            
        Returns:
            bool: True if updated successfully
        """
        updates = []
        params = []
        
        if full_name is not None:
            if not self.validator.validate_string(full_name, min_length=1):
                raise ValueError("Full name cannot be empty")
            updates.append("full_name = ?")
            params.append(full_name)
        if email is not None:
            if not self.validator.validate_email(email):
                raise ValueError("Invalid email format")
            updates.append("email = ?")
            params.append(email)
        if phone is not None:
            updates.append("phone = ?")
            params.append(phone)
        
        if not updates:
            return False
        
        params.append(member_id)
        query = f"UPDATE members SET {', '.join(updates)} WHERE member_id = ?"
        
        try:
            affected = self.db.execute_update(query, tuple(params))
            if affected > 0:
                print(f"✓ Member {member_id} updated successfully")
                return True
            return False
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Email is already in use")
            raise
    
    def delete_member(self, member_id):
        """
        Delete a member.
        
        Args:
            member_id (int): Member ID
            
        Returns:
            bool: True if deleted successfully
        """
        query = "DELETE FROM members WHERE member_id = ?"
        affected = self.db.execute_delete(query, (member_id,))
        if affected > 0:
            print(f"✓ Member {member_id} deleted successfully")
            return True
        print(f"✗ Member {member_id} not found")
        return False
