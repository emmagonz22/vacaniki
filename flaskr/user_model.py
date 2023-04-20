from flask_login import UserMixin
from flaskr.backend import Backend
from enum import Enum

class Role(Enum):
    ADMIN=1
    USER=2
"""User model for the 

User model extending the UserMixin class with feature to add more custom data from the User

Typical usage example:

  user = User(username)
  isActiveUser = user.is_active() 
"""
class User(UserMixin):

    def __init__(
        self,
        username: str
    ):

        #create a unique id using the username input to load user session
        self.username: str = username
        self.id: str = username
        # Retrieve USer data from GCS
        backend: Backend = Backend()
        user_data: dict = backend.get_user_data(self.username)
        self.email: str = user_data.get("email")
        self.name: str = user_data.get("name")
        self.description: str = user_data.get("description")
        self.role= user_data.get("role") if user_data.get("role") else Role.USER

    #returns User
    @staticmethod
    def get(username):
        return User(username=username)

    """
    Convert the User object to string with user basic information
    """

    def __str__(self):
        return f"User: {self.username}"
        #, Full name: {self.first_name} {self.second_name}, Description {self.description}"

    def is_admin(self):
        return self.role == 1