from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

UPLOAD_FOLDER = 'static/img'  # Define where to save uploaded files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = os.urandom(24) #change it later, for sure
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./gameStore.db'

    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)
    
    @app.before_request
    def create_tables_and_add_placeholder():
        # Create all tables if they don't exist yet
        db.create_all()

        # Check if the "items" table is empty and add a placeholder if necessary
        from models import Item  # Import your model here to avoid circular import issues
        if not Item.query.first():  # If no items in the table
            placeholder_item = Item(invRef='Potentially your first item!', title='Inventory can''t be empty :)', price=320, condition="New", image="static/img/no_image.png")
            db.session.add(placeholder_item)
            db.session.commit()

    return app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS