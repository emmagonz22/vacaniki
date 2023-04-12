from flask_login import UserMixin
from flaskr.backend import Backend
"""User model for the 

User model extending the UserMixin class with feature to add more custom data from the User

Typical usage example:

  user = User(username)
  isActiveUser = user.is_active() 
"""


class User(UserMixin):

    def __init__(
        self,
        username: str,
    ):

        #create a unique id using the username input to load user session
        self.username: str = username

        # Retrieve USer data from GCS
        backend = Backend()
        user_data = backend.get_user_data(self.username)
        print(user_data)

        self.id = user_data.get("username")
        self.email: str = user_data.get("email")
        self.name: str = user_data.get("name")
        self.description: str = user_data.get("description")

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
