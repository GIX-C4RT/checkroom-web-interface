from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for
)
from werkzeug.exceptions import abort
import cv2

from checkroom.auth import admin_required
from checkroom.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

# make all admin routes admin required
@bp.before_request
@admin_required
def before_request():
    '''Protect all of the admin endpoints'''
    pass

@bp.route("/")
def index():
    db = get_db()
    items = db.execute(
        'SELECT i.id, name, description, borrower, username'
        ' FROM item i'
        ' LEFT JOIN user u ON i.borrower = u.id'
        ' ORDER BY name ASC'
    ).fetchall()
    return render_template('admin/index.html.jinja', items=items)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_file = request.files['image']
        
        error = None

        if not name:
            error = 'Name is required'
        if image_file.filename == '':
            error = 'Image is required'
        
        if error is not None:
            flash(error)
        else:
            # serialize image for storage
            image_serialized = image_file.read()
            # print(image_serialized)
            db = get_db()
            db.execute(
                'INSERT INTO item (name, description, image) VALUES (?, ?, ?)',
                (name, description, image_serialized)
            )
            db.commit()
            return redirect(url_for('admin.index'))
    return render_template('admin/create.html.jinja')

def get_item(id):
    item = get_db().execute(
        'SELECT id, name, description FROM item WHERE id = ?',
        (id,)
    ).fetchone()

    if item is None:
        abort(404, f"Item id {id} doesn't exist.")
    
    return item

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    item = get_item(id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_file = request.files['image']
        # print(image_file)

        error = None

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            if image_file.filename != '':
                # print("updating image")
                # serialize image for storage
                image_serialized = image_file.read()
                db.execute(
                    'UPDATE item SET name = ?, description = ?, image = ?'
                    ' WHERE id = ?',
                    (name, description, image_serialized, id)
                )
            else:
                # print("not updating image")
                db.execute(
                    'UPDATE item SET name = ?, description = ?'
                    ' WHERE id = ?',
                    (name, description, id)
                )
            db.commit()
            return redirect(url_for('admin.index'))

    return render_template('admin/update.html.jinja', item=item)

@bp.route('delete/<int:id>', methods=('POST',))
def delete(id):
    get_item(id)
    db = get_db()
    db.execute('DELETE FROM item WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin.index'))