# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
from flask import Flask, request, redirect, url_for, render_template
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
    
    @app.route("get_wiki_page")
    def get_wiki_page(self, name):
        content_blobs = self.storage_client.list_blobs(self.bucket_content.name)
        wiki_page = None
        for blob in content_blobs:
            if blob.name == name:
                wiki_page = blob
                break
        return render_template("get_wiki_page.html", wiki_page=wiki_page) # Wiki not found in bucket

    @app.route("/get_all_page_names")
    def get_all_page_names(self):#List of content in blob (pages) 
        content_blobs = self.storage_client.list_blobs(self.bucket_content.name)
        page_list = []
        for blob in content_blobs:
            page_list.append(blob.name)
        return render_template("get_all_page_names.html", page_list=page_list)

    @app.route("/upload/", method=["GET","POST"])
    def upload(self): #Add content to the content-bucket (a blob object)
        new_page_blob = self.bucket_content.blob("New page")
        if request.method == "POST":
            with new_page_blob.open("w") as new_page:
                new_page.write(request.form["page"])
            return redirect()
        else:
            return 
    # For testing purpose 
    def upload_page(self):
       new_page_blob = self.bucket_content.blob("Test page")
       new_page = Page("Test page", ["Content"], None)
       with new_page_blob.open("w") as add_new_page:
           add_new_page.write(new_page)

    @app.route("/signup/", method=["GET","POST"])
    def sign_up(self):
        new_user_blob = self.bucket_user_password.blob("name?")
        if request.method != "POST":
            print("Invalid method request")
        else:
            username: str = request.form["username"]
            password: str = request.form["password"]
            hash_password: str = "blake2b_"+hashlib.blake2b(password)
            user = User(username, hash_password)
            if not self.bucket_user_password.blob(username):
                with new_user_blob.open("w") as new_user:
                    new_user.write(user)
            else:
                print(f"User {username} already exist")
            
    @app.route("/signin/", method=["GET","POST"])
    def sign_in(self):
        if request.method != "POST":
            print("Invalid method request")
        else:
            username = request.form["username"]
            password = request.form["password"]
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
        return render_template("signin.html")
    
    @app.route("/get_image/", method=["GET"])
    def get_image(self):
        pass

