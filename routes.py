from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
import os
from models import Item, User
from PIL import Image, ExifTags
from app import allowed_file

def compress_image(image_path):
    with Image.open(image_path) as img:
        try:
            exif = img._getexif()
            if exif is not None:
                for tag, value in exif.items():
                    if ExifTags.TAGS.get(tag) == 'Orientation':
                        if value == 3:
                            img = img.rotate(180, expand=True)
                        elif value == 6:
                            img = img.rotate(270, expand=True)
                        elif value == 8:
                            img = img.rotate(90, expand=True)
                        break
        except (AttributeError, KeyError, IndexError):
            # No EXIF data or EXIF is not available, so we skip
            pass

        img = img.convert('RGB')  # Ensure the image is in RGB mode (for .jpg compression)
        img.thumbnail((800, 800))  # Resize the image (maximum size 800x800px)
        img.save(image_path, quality=85, optimize=True) 

def register_routes(app, db, bcrypt):
    @app.route('/')
    def index():    
        

        return render_template('index.html' )
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'GET':
            return render_template('register.html')        
        elif request.method == 'POST':
            username = request.form.get('username')           
            password = request.form.get('password')  
            second_password = request.form.get('password-confirm')
            if (password == second_password):
                hashed_password = bcrypt.generate_password_hash(password)

                user = User(username=username, password=hashed_password)

                db.session.add(user)

                db.session.commit()
                return redirect(url_for('index'))
            else:
                return 'Passwords don''t match'
    

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')        
        elif request.method == 'POST':
            username = request.form.get('username')           
            password = request.form.get('password')  

            user = User.query.filter(User.username == username).first()

            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return 'Failed'

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))    
    
    @app.route('/inventory_search', methods=['GET','POST'])
    @login_required
    def inventory_search():   
        query = request.args.get('query', '')  # Get search query from URL
    
        if query:
            # Search by inventory reference or title (case-insensitive search)
            items = Item.query.filter(
                (Item.invRef.ilike(f'%{query}%')) |  # Search by inventory reference
                (Item.title.ilike(f'%{query}%'))    # Search by title
            ).all()
        else:
            # If no query, just show all items
            items = Item.query.all()

        return render_template('inventory_search.html',items=items)
        
    @app.route('/inventory', methods=['GET', 'POST'])
    @login_required
    def inventory():
        if request.method == 'GET':
            items = Item.query.all()
            return render_template('inventory.html', items=items)

        elif request.method == 'POST':
            invRef = request.form.get('invRef')
            title = request.form.get('title')
            price = request.form.get('price')
            image = request.files.get('image') 
            condition = request.form.get('condition')

            if not (title and price and invRef):
                flash("All fields are required!", "error")
                return redirect(url_for('inventory'))

            image_filename = None
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                compress_image(image_filename)

            else:
            # Default image
                image_filename = "static/img/no_image.png"

            # Save the item to the database
            item = Item(invRef=invRef, condition=condition, title=title, price=price, image=image_filename)
            db.session.add(item)
            db.session.commit()

            flash("Item created successfully!", "success")
            return redirect(url_for('inventory'))
    
    @app.route('/delete/<pid>', methods=['DELETE'])
    @login_required
    def delete(pid):
        item = Item.query.get(pid)

        image_path = item.image

        if image_path and image_path != 'static/img/no_image.png':
            try:
                # Check if the file exists, then delete it
                if os.path.exists(image_path):
                    os.remove(image_path)
            except Exception as e:
                print(f"Error deleting image: {e}")

        Item.query.filter(Item.pid == pid).delete()

        db.session.commit()

        items = Item.query.all()

        return render_template('index.html', items=items)
    
    @app.route('/details/<int:pid>')
    @login_required
    def details(pid):
        # Fetch the item from the database by its primary key (pid)
        item = Item.query.get(pid)

        # If item doesn't exist, redirect or show an error
        if item is None:
            return redirect(url_for('inventory'))
        
        # Pass the item to the template
        return render_template('details.html', item=item)
    
    @app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
    @login_required
    def edit_item(item_id):
        # Retrieve the specific item
        item = Item.query.get_or_404(item_id)

        if request.method == 'POST':
            # Update item details from form submission
            item.title = request.form['title']
            item.price = float(request.form['price'])
            item.invRef = request.form['invRef']
            item.condition = request.form['condition']

            try:
                db.session.commit()
                flash('Item updated successfully!', 'success')
                return redirect(url_for('inventory'))  # Redirects to inventory page
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating item: {str(e)}', 'danger')

        # Render edit form with existing item data
        return redirect(url_for('inventory'))

    