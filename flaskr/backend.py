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

    def upload_user_profile_picture(
            self, username: str, image_name: str,
            image: str):  #Add content to the content-bucket (a blob object)
        """Upload image format file to the GCS username-data bucket.

        Upload image file to the GCS username-data bucket if the user already have a profile picture then is going to overwrite the image.

        Args:
            image_name:
                Name of the image that is going to be uploaded.
            image:
                Image that is going to be uploaded (Images [png, jpeg])
        
        """

        new_image_blob = self.user_data_bucket.blob(image_name)
        new_image_blob.upload_from_file(image, content_type=image.content_type)

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
                'description': ''
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

    def get_image(self, name: str, bytes_io=BytesIO):
        """Query image from the GCS's content bucket.

        Query image from the GCS's content bucket.

        Args:
            name:
                The image's blob name (not file name) 

        Returns:
            Image data from the blob with name of the parameter 'name'

        """

        image_blob = self.bucket_content.get_blob(name)

        content_byte = image_blob.download_as_bytes()

        return bytes_io(content_byte)

    """Query user data from the Google cloud storage
    
    Query user data from the Google cloud storage, if the user doesn't exist in the username-data bucket raise Exception "User doesn't exist"

    Args:
        username:
            The desired user's data to return

    """

    def get_user_data(self, username):
        data_blob = self.user_data_bucket.get_blob(username)
        if not data_blob:
            return {'username': username}
        data = data_blob.download_as_text()
        print(json.loads(data))
        return json.loads(data)

    def upload_file_registry(self, username):
        ''' Upload user file registry onto their json profile-data file

        Appends user uploads from wiki-content bucket onto the user profile-data json file to be added to the user data bucket

        Args:
            username:
                The desired user's username to be updated
        '''
        user_json = self.get_user_data(username)
        uploads_blob = self.bucket_content.list_blobs(prefix=f'{username}/')

        # lists to store the name of uploaded pages and images of the user
        wiki_pages = user_json.get("uploaded_wiki", [])
        images = user_json.get("uploaded_image", [])

        # set used to check if content is already in the json data
        content_in_json = set(wiki_pages).union(images)

        # if the blob type is a html, append to the wiki pages list else, append to images
        if uploads_blob:
            for blob in uploads_blob:
                file_name = os.path.basename(blob.name)
                if file_name in content_in_json:
                    continue
                elif blob.content_type == "text/html":
                    wiki_pages.append(file_name)
                else:
                    images.append(file_name)

        # adds new information into the lists inside the json file
        user_json["uploaded_wiki"] = wiki_pages
        user_json["uploaded_image"] = images

        # adds json back into the json file
        json_file_name = f'{username}-data.json'
        with open(json_file_name, 'w') as f:
            json.dump(user_json, f)

        # upload json content back into the content
        blob = self.user_data_bucket.blob(f"{username}")
        blob.upload_from_filename(json_file_name)