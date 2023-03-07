from flask_login import UserMixin
import hashlib

"""User model for the 

User model extending the UserMixin class with feature to add more custom data from the User

Typical usage example:

  user = User(username)
  isActiveUser = user.is_active() 
"""


class User(UserMixin):

    def __init__(self, username: str, 
                email: str = "", id: str = "",
                first_name: str = "", second_name: str = "", 
                description:str ="",
                profile_picture: str = None):

        #create a unique id using the username input to load user session
        self.username: str = username
        self.id = hashlib.blake2b(username.encode('utf-8')).hexdigest()
        print("USERNAME", self.username)
        self.email: str = email
        self.first_name: str = first_name
        self.second_name: str = second_name
        self.description: str = description 
        self.profile_picture = profile_picture

    #returns User
    @staticmethod
    def get(user_id):
        return User(user_id)

    """
    Convert the User object to string with user basic information
    """
    def __str__(self):
        return f"User: {self.username}"
        #, Full name: {self.first_name} {self.second_name}, Description {self.description}"


