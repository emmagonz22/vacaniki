# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
from user_model import User
from page_model import Page
import hashlib


"""


"""
class Backend:

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_content = self.storage_client.bucket("wikiviewer-content")
        self.bucket_user_password = self.storage_client.bucket("user-passwords")
    

    def get_wiki_page(self, name):
        content_blobs = self.storage_client.list_blobs(self.bucket_content.name)
        wiki_page = None
        for blob in content_blobs:
            if blob.name == name:
                wiki_page = blob
                break
        return wiki_page

    def get_all_page_names(self):#List of content in blob (pages) 
        content_blobs = self.storage_client.list_blobs(self.bucket_content.name)
        page_list = []
        for blob in content_blobs:
            page_list.append(blob.name)
        return page_list

        
    def upload(self): #Add content to the content-bucket (a blob object)
        new_page_blob = self.bucket_content.blob("New page")
        with new_page_blob.open("w") as f:
            f.write("Upload")

    # For testing purpose 
    def upload_page(self):
       new_page_blob = self.bucket_content.blob("Test page")
       new_page = Page("Test page", ["Content"], None)
       with new_page_blob.open("w") as add_new_page:
           add_new_page.write(new_page)

    def sign_up(self):
        new_user_blob = self.bucket_user_password.blob("name?")
        username: str = 1
        password: str = 1
        hash_password: str = "blake2b_"+hashlib.blake2b(password)
        user = User(username, hash_password)
        if not self.bucket_user_password.blob(username):
            with new_user_blob.open("w") as new_user:
                new_user.write(user)
        else:
            print(f"User {username} already exist")
        
    def sign_in(self):
 
        username = 1
        password = 1
        hash_password: str = "blake2b_"+hashlib.blake2b(password)
        user = User(username, hash_password)

        if self.bucket_user_password.blob(username):
            read_user_blob = self.bucket_user_password.blob(username)
            with read_user_blob.open("r") as user_signin:
                print(user_signin.read())
                if user_signin.username == user.username and user_signin.hash_password == user.hash_password:
                    print("Successful sign in")
        else:
            raise Exception(f"Wrong {username} or password")

    def get_image(self):
        pass

