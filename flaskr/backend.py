# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import hashlib
from io import BytesIO
import os
import json
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

    def __init__(self, storage_client=storage.Client()):
        self.storage_client = storage_client
        self.bucket_content = self.storage_client.bucket("wikiviewer-content")
        self.bucket_user_password = self.storage_client.bucket("user-passwords")
        self.user_data_bucket = self.storage_client.bucket("username-data")

    def get_wiki_page(self, name):
        """Get wiki page with specific name

        Query the wiki page with specific name from the GCS's content bucket
        and download it in the templates folder location with {name}.

        Returns:
            Wikipage with designated name.

        """
        wiki_blob = self.bucket_content.blob(name)

        if wiki_blob.exists(self.storage_client):
            with wiki_blob.open("r") as page:
                return page.read()
            #file_path = f"flaskr/templates/{name}"
            #wiki_blob.download_to_filename(file_path)
            #return (wiki_blob, wiki_blob.content_type, file_path, name)

        return None

    def get_all_page_names(self):  #List of content in blob (pages)
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

    def upload(self, content_name,
               content):  #Add content to the content-bucket (a blob object)
        """Upload content to the GCS content bucket.

        Upload content to the GCS content bucket if the data already exist is going to overwrite the content.

        Args:
            content_name:
                Name of the content that is going to be uploaded.
            content:
                File that is going to be uploaded (Images [png, jpeg, etc], html file, css file, etc)
        
        """

        new_blob = self.bucket_content.blob(content_name)
        new_blob.upload_from_file(content, content_type=content.content_type)

    def upload_user_profile_picture(self, username, content_name,
               content):  #Add content to the content-bucket (a blob object)
        """Upload content to the GCS content bucket.

     
        Upload content to the GCS content bucket in prefix named given username and if the data already exist is going to overwrite the content.

        Args: 
            username:
                Prefix to upload content 
            content_name:
                Name of the content that is going to be uploaded.
            content:
                File that is going to be uploaded (Images [png, jpeg, etc], html file, css file, etc)
        
        """

        new_page_blob = self.bucket_content.blob(f"{username}/{content_name}")
        new_page_blob.upload_from_file(content,
                                       content_type=content.content_type)


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
        hash_password: str = hashlib.blake2b(
            salted_password.encode()).hexdigest()

        if not new_user_blob.exists(self.storage_client):
            print("Account doesn't exist")

            # Creating json file with basic user-data
            user_data = {
                'username': username,
                'name': '',
                'email': '',
                'uploaded_wiki': [],
                'uploaded_image': [],
                'created_at': '',
                'description': '',
                'profile_photo': False
            }
            blob = self.user_data_bucket.blob(f"{username}")

            json_file_name = f'{username}-data.json'
            with open(json_file_name, 'w') as f:
                json.dump(user_data, f)
            blob.upload_from_filename(json_file_name)
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
        hash_password: str = hashlib.blake2b(
            salted_password.encode()).hexdigest()
        user_blob = self.bucket_user_password.blob(username)
        if user_blob.exists(self.storage_client):
            with user_blob.open("r") as user_signin:

                if user_signin.read() == hash_password:
                    return True

        return False

    def get_image(self, name: str, prefix="", bytes_io=BytesIO):
        """Query image from the GCS's content bucket.

        Query image from the GCS's content bucket.

        Args:
            name:
                The image's blob name (not file name) 

        Returns:
            Image data from the blob with name of the parameter 'name'

        """
        if prefix == "":
            image_blob = self.bucket_content.get_blob(name)
        else:
            blobs = self.storage_client.list_blobs(self.bucket_content.name, prefix=prefix)
            #blobs = self.bucket_content.list_blobs(prefix=prefix)
           
            for blob in blobs:
                if blob.name.endswith(name):
                    print(blob.name, name)
                    image_blob = blob
                    break
            else:
            # The loop completed without finding the blob, so raise an error
                raise ValueError(f"No blob found with prefix/name {prefix}/{name}")
    
        if image_blob is None:
            raise ValueError(f"No blob found with prefix/name {prefix}/{name}")

        content_byte = image_blob.download_as_bytes()

        return bytes_io(content_byte)

  

    def get_user_data(self, username):
        """Query user data from the Google cloud storage
    
        Query user data from the Google cloud storage, if the user doesn't exist in the username-data bucket raise Exception "User doesn't exist"

        Args:
            username:
                The desired user's data to return

        """
        data_blob = self.user_data_bucket.get_blob(username)
        if not data_blob:
            return {'username': username}
        data = data_blob.download_as_text()
        #print(json.loads(data))
        return json.loads(data)

    def edit_user(self, username,  name, description, image):
        """Modify user data from GCS
    
        Get user with given username and replace is name, description and profile picture

        Args:
            username:
                The desired user's data to edit
            name:
                New name (string) for the deserid user
            description:
                New description (string) for the user
            image:
                New profile picture for the user
        """

        data_blob = self.user_data_bucket.get_blob(username)
        if not data_blob:
            return False
       
       # download json as string 
        blob_content = data_blob.download_as_string()

        # convert to dictionary
        data = json.loads(blob_content)

        data['name'] = name
        data['description'] = description
        data['profile_photo'] = True
        
    
        #COnvert to json
        new_data_json = json.dumps(data).encode('utf-8')
        data_blob.upload_from_string(new_data_json)

        #Upload image
        self.upload_user_profile_picture(username, "profile_pic", image)

        return True

