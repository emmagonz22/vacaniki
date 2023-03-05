from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from google.cloud import storage
from flaskr.backend import Backend
import hashlib

def make_endpoints(app):
    # create an instance of the Backend class
    backend = Backend()


    @app.route("/")
    def home():
        return render_template('main.html')


    @app.route('/signup/', methods=['GET', 'POST'])
    def sign_up():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username: str = request.form['username'].lower()
            password: str = request.form['password']

            # sends user and pass to backend to be verified/sent to bucket and signed in
            backend.sign_up(username=username, password=password)
            print('Signed up successfully!')
            return render_template('main.html')
        else:
            return 'Invalid method request'


    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        if request.method == "GET":
            return render_template('login.html')
        elif request.method == 'POST':
            username: str = request.form['username'].lower()
            password: str = request.form['password']

            # sends user and pass to backend to be verified and logged in
            backend.sign_in(username=username, password=password)
            print('Logged in successfully!')
            return render_template('main.html')
        else: 
            return 'Invalid method request'


    @app.route('/logout/', methods=['GET'])
    def logout():
        # using flask-login module, logouts user and redirects to home page
        logout_user()
        return redirect(url_for('home'))


    @app.route('/upload/', methods=['GET','POST'])
    def upload():
        if request.method == 'POST':
            if 'file' not in request.files:
                print('No File Input')
                return redirect(url_for('upload'))

            #grab wikipage name and file content
            wikipage: str = request.form['wikipage']
            file = request.files['file']
            if file.filename == '':
                print('No selected file')
                return redirect(url_for('upload'))
            if file:
                backend.upload(wikipage, file)
                print('File uploaded successfully')
                return render_template('main')
        return render_template('upload.html')