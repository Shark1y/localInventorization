from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import redirect, url_for
import os

UPLOAD_FOLDER = 'static/img'  # Images are saved here
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # Allowed image extensions

db = SQLAlchemy() # Initialize database

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    app.secret_key = os.urandom(24) #change it later, for sure 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./gameStore.db' # Access to local database

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User # import user model

    @login_manager.user_loader    
    def load_user(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler # If user doesn't have access to certain pages
    def unauthorized_callback():
        return redirect(url_for('index'))

    bcrypt = Bcrypt(app) # password encryption

    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS