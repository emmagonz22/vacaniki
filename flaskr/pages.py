from flask import Flask, redirect, render_template, request, url_for, flash, send_file, render_template_string
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from google.cloud import storage
from flaskr.backend import Backend
from flaskr.user_model import User
import hashlib
import werkzeug
from io import BytesIO


def make_endpoints(app):
    # create an instance of the Backend class
    backend = Backend()

    @app.route("/")
    def home():
        """Returns homepage."""
        return render_template(
            'main.html',
            page_name="Vacationiki",
            page_content="One stop shop for the greatest vacation sites!",
        )

    @app.route("/about")
    def about():
        """Returns about page."""
        return render_template('about.html')

    @app.route("/images/<img_blob_name>")
    def images(img_blob_name):
        """Returns image from from `get_image()` method."""
        #return img_blob_name
        if current_user.is_authenticated and img_blob_name == "profile_pic":
            img = backend.get_image(img_blob_name, prefix=current_user.username)
        else:
            img = backend.get_image(img_blob_name)

        if img_blob_name.endswith('.jpeg') or img_blob_name.endswith('.jpg'):
            mimetype = 'image/jpeg'
        else:
            mimetype = 'image/png'

        print("Loading image with mime: ", mimetype, img)
        return send_file(img, mimetype=mimetype)

    @app.route("/pages")
    def all_pages():
        """Returns all of the pages from `get_all_page_names()` method."""
        return render_template("pages.html",
                               page_name="Vactioniki Index",
                               all_pages=backend.get_all_page_names())

    @app.route("/pages/<name>")
    def page(name):
        """Returns the page from `get_wiki_page()` method."""
        wiki_page = backend.get_wiki_page(name)
        return render_template_string(
            wiki_page,
            page_name=name,
        )

    @app.route('/signup/', methods=['GET', 'POST'])
    def sign_up():
        '''Returns signup page'''
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username: str = request.form['username'].lower()
            password: str = request.form['password']

            # sends user and pass to backend to be verified/sent to bucket and signed in
            sign_up_event = backend.sign_up(username=username,
                                            password=password)
            if sign_up_event:

                user = User(username=username)
                login_user(user)
                flash('Signed up successfully!')
                flash(str(user))
                return redirect(url_for('home'))
            else:
                flash('Account already exist!')
                return redirect(url_for('sign_up'))
        else:
            return redirect(url_for('sign_up'))

    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        '''Returns login page'''
        if request.method == "GET":
            print("Rendering login template")
            return render_template('login.html')
        elif request.method == 'POST':
            username: str = request.form['username'].lower()
            password: str = request.form['password']

            # sends user and pass to backend to be verified and logged in
            sign_in_event = backend.sign_in(username=username,
                                            password=password)
            print("Signin USER: ", username)
            if sign_in_event:
                user = User(username=username)
                login_user(user)

                flash('Logged in successfully.')
                return redirect(url_for("home"))
            else:
                flash('Wrong username or password. Please Try Again.')
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))

    @login_required
    @app.route('/logout/', methods=['GET'])
    def logout():
        '''logouts current user and redirects to home'''
        # using flask-login module, logouts user and redirects to home page
        logout_user()
        flash('Logged out')
        return redirect(url_for('home'))

    @login_required
    @app.route('/upload/', methods=['GET', 'POST'])
    def upload():
        '''Returns upload page'''
        if request.method == 'GET':
            return render_template('upload.html')
        else:
            if 'file' not in request.files:
                flash('No File Input')
                return redirect(url_for('upload'))
            elif request.files[
                    'file'].content_type == "text/html" and not current_user.is_admin(
                    ):
                flash('No admin privileges')
                print(current_user.role)
                return redirect(url_for('upload'))

            #grab wikipage name and file content
            wikipage: str = request.form['wikipage']
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('upload'))
            if file:
                backend.upload(wikipage, file)
                flash('File uploaded successfully')
                return redirect(url_for('upload'))

    @app.route('/delete/', methods=['GET'])
    def delete_user():
        backend.delete_user_uploads(current_user.username)
        success_user = backend.delete_user(current_user.username)
        if success_user:  # checks if the user deletion was successful
            logout_user()
            flash('Successfully deleted user')
        else:
            # if something wrong happens, print an error and redirect
            flash('Something went wrong')
            redirect(url_for('home'))

        return redirect(url_for('home'))

    @login_required
    @app.route('/profile/<username>', methods=['GET', 'POST'])
    def profile_view(username):
        if current_user.is_authenticated:
            username = current_user.username
            user_data = backend.get_user_data(current_user.username)
            return render_template('profile_view.html', user_data=user_data)
        else:
            return redirect(url_for('login'))

    @login_required
    @app.route('/edit-user', methods=['GET', 'POST'])
    def edit_user():
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if request.method == 'GET':
            return redirect(
                url_for('profile_view', username=current_user.username))
        else:
            # Get the form data
            name = request.form.get('name')
            description = request.form.get('description')
            image = request.files.get('image')
            if backend.edit_user(current_user.username, name, description,
                                 image):
                print("User updated Successfully")
            else:
                print("Error updating user")

            return redirect(
                url_for('profile_view', username=current_user.username))
        return 'Form not submitted successfully'

    @app.route('/template', methods=['GET'])
    def template():
        return render_template('boqueron-beach.html')
