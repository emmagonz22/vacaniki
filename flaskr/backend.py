# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import hashlib
from base64 import b64encode
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
            if blob.content_type == "text/html":
                page_list.append(blob.name)
        return page_list

    
    def upload(self, content_name, content): #Add content to the content-bucket (a blob object)
        """Upload content to the GCS content bucket.

        Upload content to the GCS content bucket if the data already exist is going to overwrite the content.

        Args:
            content_name:
                Name of the content that is going to be uploaded.
            content:
                File that is going to be uploaded (Images [png, jpeg, etc], html file, css file, etc)
        
        """  
        new_page_blob = self.bucket_content.blob(content_name)
        new_page_blob.upload_from_file(content)


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

        if not new_user_blob.exists(self.storage_client):
            print("Account doesn't exist")
            with new_user_blob.open("w") as new_user:
                new_user.write(hash_password)
                return True
        else:
            print(f"User {username} already exist")
            return False


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
        user_blob = self.bucket_user_password.blob(username)
        if user_blob.exists(self.storage_client):
            
            with user_blob.open("r") as user_signin:

                if user_signin.read() == hash_password:
                    return True
        
        return False

    def get_image(self, name: str):
        """Query image from the GCS's content bucket.

        Query image from the GCS's content bucket.

        Args:
            name:
                The image's blob name (not file name) 

        Returns:
            A tuple with the corresponding image and content_type of the blob, if not found return Image not Found

        """  

    
        image_blob = self.bucket_content.blob(name)

        if image_blob.exists(self.storage_client):
            #
            return b64encode(image_blob.download_as_bytes()).decode("utf-8") ## Content type can be use for image format
        return "Image not Found" ## This can change to an raise Exception
