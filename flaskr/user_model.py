from flask_login import UserMixin


"""User model for the 

User model extending the UserMixin class with feature to add more custom data from the User

Typical usage example:

  user = User(username, password)
  isActiveUser = user.is_active() 
"""


class User(UserMixin):

    def __init__(self, username: str, hash_password: str, 
                email: str = "",
                first_name: str = "", second_name: str = "", 
                description:str ="",
                profile_picture: str = None):
        self.username: str = username
        self.email: str = email
        #Using the hashlin blake2b with prefix blake2b_<hash>
        self.hash_password: str = hash_password
        self.first_name: str = first_name
        self.second_name: str = second_name
        self.description: str = description 
        self.profile_picture = profile_picture

    """
    Convert the User object to string with user basic information
    """
    def __str__(self):
        return f"User: {self.username}, Full name: {self.first_name} {self.second_name}, Description {self.description}"