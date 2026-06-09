"""Member model for library management system."""

class Member:
    """Represents a library member."""
    
    def __init__(self, member_id, full_name, email, phone):
        """
        Initialize a Member instance.
        
        Args:
            member_id (int): Unique identifier for the member
            full_name (str): Full name of the member
            email (str): Email address
            phone (str): Phone number
        """
        self.member_id = member_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
    
    def __repr__(self):
        return f"Member(id={self.member_id}, name='{self.full_name}', email='{self.email}')"
    
    def to_dict(self):
        """Convert member to dictionary."""
        return {
            'member_id': self.member_id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone
        }
