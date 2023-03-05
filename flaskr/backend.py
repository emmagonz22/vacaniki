# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import hashlib
from user_model import User 
from page_model import Page

"""Backend class for the `Vacapedia` platform

Backend class for the `Vacapedia` platform, this class can add, verify if 
the user exist with certain credentials in the user to the Google Cloud Storage.
This class import the google cloud storage and the model use to manage the information 
in the backend.

Typical usage example:

  backend = Backend()
  wiki_pages_list = backend.get_all_page_names()
"""
class Backend:

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_content = self.storage_client.bucket("wikiviewer-content")
        self.bucket_user_password = self.storage_client.bucket("user-passwords")
        self.active_user: User = None


    def get_wiki_page(self, name):
        """Get wiki page with specific name

        Query the wiki page with specific name from the GCS's content bucket.

        Returns:
            List with all the names

        """  
        content_blobs = self.storage_client.list_blobs(self.bucket_content.name)
        wiki_page = None
        for blob in content_blobs:
            if blob.name == name:
                wiki_page = blob
                break
        return wiki_page

    def get_all_page_names(self):#List of content in blob (pages) 
        """Query all the pages from the GCS's content bucket.

        Query all the pages name from the GCS's content bucket.

        Returns:
            List with all the names

        """  
        content_blobs = self.storage_client.list_blobs(self.bucket_content.name)
        page_list = []
        for blob in content_blobs:
            page_list.append(blob.name)
        return page_list

    
    def upload(self, content_name, content): #Add content to the content-bucket (a blob object)
        """Upload content to the GCS content bucket.

        Upload content to the GCS content bucket if the data already exist is going to overwrite the content.

        Args:
            content_name:
                Name of the content that is going to be uploaded.
            content:
                Content that is going to be uploaded.
        
        """  

        new_page_blob = self.bucket_content.blob(content_name)
        with new_page_blob.open("w") as f:
            f.write(content)


    def sign_up(self, username: str, password: str):
        """Create new account in the GCS's user-password bucket.

        Add new account as a blob to the GCS's storage, if the accoutn already exist it raise and Exception

        Args:
            username:
                New user's username
            password:
                New user's password
        
        Raises:
            AccountAlreadyExist: The username is already taken.

        """  
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
        """Verify credential in the GCS's user-password bucket

        Verify if the user exist in the user-password storage and verify if the password is correct

        Args:
            username:
                User's username
            password:
                User's password
        """  
        #Salt added to increase security in the password
        salted_password: str = f"{username}_vacation2023_{password}"
        #Hash saltes password wuth the blake2b hash function
        hash_password: str = hashlib.blake2b(salted_password.encode()).hexdigest() 
        
        if self.bucket_user_password.blob(username):
            read_user_blob = self.bucket_user_password.blob(username)
            with read_user_blob.open("r") as user_signin:
                print(user_signin.read())
                if user_signin.username == username and user_signin.hash_password == hash_password:
                    print("Successful sign in")
                    self.active_user = user_signin
        else:
            raise Exception(f"Wrong {username} or password")

    def get_image(self, image_name: str):
        """Query image from the GCS's content bucket.

        Query image from the GCS's content bucket.

        Args:
            image_name:
                The image name 

        Returns:
            A image object? with the corresponding name of image_name

        Raise:
            ImageNotFound: 
                Image not found in the cloud storage
        """  
        read_blob = self.bucket_content.blob(image_name)
        with read_blob.open("r") as image:
            return image.read()
        
