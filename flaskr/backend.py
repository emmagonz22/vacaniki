# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import hashlib
from user_model import User 
from page_model import Page

"""


"""
class Backend:

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_content = self.storage_client.bucket("wikiviewer-content")
        self.bucket_user_password = self.storage_client.bucket("user-passwords")
        self.active_user: User = None
    """

    """
    def get_wiki_page(self, name):
        content_blobs = self.storage_client.list_blobs(self.bucket_content.name)
        wiki_page = None
        for blob in content_blobs:
            if blob.name == name:
                wiki_page = blob
                break
        return wiki_page
    """


    """
    def get_all_page_names(self):#List of content in blob (pages) 
        content_blobs = self.storage_client.list_blobs(self.bucket_content.name)
        page_list = []
        for blob in content_blobs:
            page_list.append(blob.name)
        return page_list

    """


    """
    def upload(self, content_name, content): #Add content to the content-bucket (a blob object)
        new_page_blob = self.bucket_content.blob(content_name)
        with new_page_blob.open("w") as f:
            f.write(content)

    """

    """
    def sign_up(self, username: str, password: str):
        new_user_blob = self.bucket_user_password.blob(username)
        salted_password = f"{username}_vacation2023_{password}"
        hash_password: str = hashlib.blake2b(salted_password.encode()).hexdigest()
        user: User = User(username, hash_password)
        if not self.bucket_user_password.blob(username):
            with new_user_blob.open("w") as new_user:
                new_user.write(user)
        else:
            print(f"User {username} already exist")
    """

    """ 
    def sign_in(self, username, password):
 
        salted_password: str = f"{username}_vacation2023_{password}"
        hash_password: str = hashlib.blake2b(salted_password.encode()).hexdigest()
        user: User = User(username, hash_password)


        if self.bucket_user_password.blob(username):
            read_user_blob = self.bucket_user_password.blob(username)
            with read_user_blob.open("r") as user_signin:
                print(user_signin.read())
                if user_signin.username == user.username and user_signin.hash_password == user.hash_password:
                    print("Successful sign in")
                    self.active_user = user_signin
        else:
            raise Exception(f"Wrong {username} or password")
    """

    """
    def get_image(self, image_name: str):
        read_blob = self.bucket_content.blob(image_name)
        with read_blob.open("r") as image:
            return image.read()
        
