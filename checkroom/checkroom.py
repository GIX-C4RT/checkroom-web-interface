from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from checkroom.auth import login_required
from checkroom.db import get_db

bp = Blueprint('checkroom', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('checkroom/index.html')

def get_items(borrower=None):
    db = get_db()
    if not borrower:
        items = db.execute(
            'SELECT id, name, description'
            ' FROM item'
            ' WHERE borrower IS NULL'
        ).fetchall()
    else:
        items = db.execute(
            'SELECT id, name, description'
            ' FROM item'
            ' WHERE borrower = ?',
            (borrower,)
        ).fetchall()

    return items

@bp.route('/checkout', methods=('GET', 'POST'))
@login_required
def checkout():
    if request.method == 'POST':
        error = None

        id = request.args.get('id')
        if id is None:
            error = "id is required."

        db = get_db()
        current_borrower = db.execute(
            'SELECT borrower'
            ' FROM item'
            ' WHERE id = ?',
            (id,)
        ).fetchone()

        if current_borrower['borrower'] is not None:
            error = "That item is unavailable."

        if error is not None:
            flash(error)
        
        db.execute(
            'UPDATE item'
            ' SET borrower = ?'
            ' WHERE id = ?',
            (g.user['id'], id)
        )
        db.commit()

        # display confirmation message
        item_name = db.execute(
            'SELECT name'
            ' FROM item'
            ' WHERE id = ?',
            (id,)
        ).fetchone()
        
        flash("Successfully checked out " + item_name["name"])

    available_items = get_items()
    # print(available_items)
    return render_template('/checkroom/checkout.html', available_items=available_items)

@bp.route('/checkin', methods=('GET', 'POST'))
@login_required
def checkin():
    if request.method == 'POST':
        error = None

        id = request.form.get('id')
        if id is None:
            error = "id is required."

        db = get_db()
        current_borrower = db.execute(
            'SELECT borrower'
            ' FROM item'
            ' WHERE id = ?',
            (id,)
        ).fetchone()
        
        if current_borrower['borrower'] != g.user['id']:
            error = "You cannot check in an item you have not checked out."

        if error is not None:
            flash(error)
        
        db.execute(
            'UPDATE item'
            ' SET borrower = NULL'
            ' WHERE id = ?',
            (id,)
        )
        db.commit()

        # display confirmation message
        item_name = db.execute(
            'SELECT name'
            ' FROM item'
            ' WHERE id = ?',
            (id,)
        ).fetchone()
        # print(item_name["name"])
        flash("Successfully checked in " + item_name["name"])

    my_items = get_items(borrower=g.user["id"])
    # print(my_items)
    return render_template('/checkroom/checkin.html', my_items=my_items)