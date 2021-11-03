from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
from werkzeug.exceptions import abort
import cv2
import numpy as np

from checkroom.auth import login_required
from checkroom.db import get_db

MAX_ITEMS = 4

bp = Blueprint('checkroom', __name__)

@bp.route('/')
@login_required
def index():
    my_items = get_items(borrower=g.user["id"])
    available_items = get_items()
    return render_template('checkroom/index.html.jinja', my_items=my_items, available_items=available_items)

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
    error = None
    if request.method == 'POST':
        # print(request.form)
        item_ids = request.form.getlist('item_ids')
        # print(ids)
        if len(item_ids) < 1:
            error = "You must select at least one item."
        elif len(item_ids) > MAX_ITEMS:
            error = "You must not select more than 4 items."
        else:
            db = get_db()
            item_names = []
            for item_id in item_ids:
                item_info = db.execute(
                    'SELECT name, borrower'
                    ' FROM item'
                    ' WHERE id = ?',
                    (item_id,)
                ).fetchone()
                item_names.append(item_info['name'])
            
                if item_info['borrower'] is not None:
                    error = f"{item_info['name']} is unavailable."
            if error is None:
                for item_id in item_ids:
                    db.execute(
                        'UPDATE item'
                        ' SET borrower = ?'
                        ' WHERE id = ?',
                        (g.user['id'], item_id)
                    )
                    db.commit()

                # display confirmation message
                success_message = f"Successfully checked out {item_names}. \
                    Please wait for the robot to bring you your item(s)."
                flash(success_message)
    if error is not None:
        flash(error)
    available_items = get_items()
    # print(available_items)
    return render_template('/checkroom/checkout.html.jinja', available_items=available_items)

@bp.route('/checkin', methods=('GET', 'POST'))
@login_required
def checkin():
    error = None
    if request.method == 'POST':
        item_ids = request.form.getlist('item_ids')
        if len(item_ids) < 1:
            error = "You must select at least one item."
        elif len(item_ids) > MAX_ITEMS:
            error = "You must not select more than 4 items."
        else:
            db = get_db()
            item_names = []
            for item_id in item_ids:
                item_info = db.execute(
                    'SELECT name, borrower'
                    ' FROM item'
                    ' WHERE id = ?',
                    (item_id,)
                ).fetchone()
                
                if item_info['borrower'] != g.user['id']:
                    error = "You cannot check in an item you have not checked out."
                item_names.append(item_info['name'])
            if error is None:
                for item_id in item_ids:   
                    db.execute(
                        'UPDATE item'
                        ' SET borrower = NULL'
                        ' WHERE id = ?',
                        (item_id,)
                    )
                    db.commit()

                # display confirmation message
                flash(f"Successfully checked in {item_names}. \
                    Please wait for the robot to retrieve your item.")
    if error is not None:
        flash(error)
    my_items = get_items(borrower=g.user["id"])
    # print(my_items)
    return render_template('/checkroom/checkin.html.jinja', my_items=my_items)

@bp.route('/aruco/<id>', methods=('GET',))
@login_required
def aruco(id):
    id = int(id)
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
    tag = np.zeros((500, 500, 1), dtype="uint8")
    cv2.aruco.drawMarker(aruco_dict, id, 500, tag, 1)
    # cv2.imshow("tag", tag)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    is_success, im_buf_arr = cv2.imencode(".png", tag)
    byte_im = im_buf_arr.tobytes()
    return Response(byte_im, mimetype="image/png")


@bp.route('/image/<id>', methods=('GET',))
@login_required
def image(id):
    id = int(id)
    db = get_db()
    image = db.execute(
        'SELECT image'
        ' FROM item'
        ' WHERE id = ?',
        (id,)
    ).fetchone()['image']
    return Response(image, mimetype="image/png")



