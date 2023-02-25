# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
from flask import Flask, request
from user_model import User
import hashlib

class Backend:

    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_content = storage.bucket("wikiviewer-content")
        self.bucket_user_password = storage.bucket("user-passwords")
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self):
        pass

    @app.route("/signup/", method=["POST"])
    def sign_up(self):
        new_user_blob = self.bucket_user_password.blob("name?")
        if request.method != "POST":
            print("Invalid method request")
        else:
            username: str = "emmagonz22"#request.form["username"]
            password: str = "123456789"#request.form["password"]
            hash_password: str = "blake2b_"+hashlib.blake2b(password)
            user = User(username, hash_password)
            if not self.bucket_user_password.blob(username):
                with new_user_blob.open("w") as new_user:
                    new_user.write(user)
            else:
                print(f"User {username} already exist")
            
    @app.route("/signin/")
    def sign_in(self):
        if request.method != "POST":
            print("Invalid method request")
        else:
            username = "emmagonz22"#request.form["username"]
            password = "123456789"#request.form["password"]
            hash_password: str = "blake2b_"+hashlib.blake2b(password)
            user = User(username, hash_password)

            if self.bucket_user_password.blob(username):
                read_user_blob = self.bucket_user_password.blob(username)
                with read_user_blob.open("r") as user_signin:
                    print(user_signin.read())
                    if user_signin.username == user.username and user_signin.hash_password == user.hash_password:
                        print("Successful sign in")
            else:
                print(f"Wrong {username} or password")


    def get_image(self):
        pass

bk = Backend()
print(f"Bucket {bk.bucket_content.name} tested")