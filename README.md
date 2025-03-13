# Vacaniki 🌍

Vacaniki is a collaborative wiki platform focused on vacation destinations around the world. Users can browse, create, and edit wiki pages about various vacation spots, upload images, and maintain user profiles.

## Description

This is the last project for the Google Tech Exchange Software Development Studio 2023.


## Getting Started

### Prerequisites

- Python 3.9 or higher
- Google Cloud SDK
- Google Cloud Storage buckets configured:
  - `wikiviewer-content` - For storing wiki pages and images
  - `user-passwords` - For storing user authentication data
  - `username-data` - For storing user profile data

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vacaniki.git
cd vacaniki
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Cloud credentials:
```bash
gcloud auth application-default login
```

### Running the Application

1. Use the provided shell script:
```bash
chmod +x run-flask.sh
./run-flask.sh
```

2. Alternatively, run the following commands:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run -p 8080
```

3. Access the application at [http://localhost:8080](http://localhost:8080)

### Deployment

The application is configured to deploy on Google Cloud App Engine:

```bash
gcloud app deploy
```

## Tech Stack

- **Backend**: Python with Flask web framework
- **Authentication**: Flask-Login for user session management
- **Storage**: Google Cloud Storage for file and data storage
- **Templating**: Jinja2 for HTML template rendering
- **Frontend**: HTML, CSS, and JavaScript
- **Testing**: Pytest for unit and integration testing
- **CI/CD**: GitLab CI/CD for continuous integration and deployment

## Project Structure

- `flaskr/` - Main application package
  - `__init__.py` - Flask application factory
  - `pages.py` - Route definitions and view functions
  - `backend.py` - Backend services for GCS interaction
  - `user_model.py` - User authentication models
  - `templates/` - Jinja2 HTML templates
  - `static/` - Static assets (CSS, images, etc.)
- `tests/` - Test suite
- `app.yaml` - Google App Engine configuration
- `requirements.txt` - Python dependencies

## Features

- **User Authentication**: Sign up, login, and profile management
- **Wiki Content**: Browse, create, and edit wiki pages
- **Image Upload**: Support for uploading images for profiles and wiki pages
- **User Profiles**: Personal profile pages with uploaded content history

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Authors

- Emmanuel Gonzalez
- Cesar Olague
- Francisco Carreon (Project Coach)
