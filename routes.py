from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from models import Item
from app import allowed_file

def register_routes(app, db):
    @app.route('/', methods=['GET','POST'])
    def index():    
        return render_template('index.html' )
        
    @app.route('/inventory', methods=['GET', 'POST'])
    def inventory():
        if request.method == 'GET':
            items = Item.query.all()
            return render_template('inventory.html', items=items)

        elif request.method == 'POST':
            invRef = request.form.get('invRef')
            title = request.form.get('title')
            price = request.form.get('price')
            image = request.files.get('image') 

            if not (title and price and invRef):
                flash("All fields are required!", "error")
                return redirect(url_for('inventory'))

            image_filename = None
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            else:
            # Default image
                image_filename = "static/img/no_image.png"

            # Save the item to the database
            item = Item(invRef=invRef, title=title, price=price, image=image_filename)
            db.session.add(item)
            db.session.commit()

            flash("Item created successfully!", "success")
            return redirect(url_for('inventory'))
    
    @app.route('/delete/<pid>', methods=['DELETE'])
    def delete(pid):
        Item.query.filter(Item.pid == pid).delete()

        db.session.commit()

        items = Item.query.all()

        return render_template('index.html', items=items)
    
    @app.route('/details/<pid>')
    def details(pid):
        item = Item.query.filter(Item.pid == pid).first()
        return render_template('details.html', item=item)
