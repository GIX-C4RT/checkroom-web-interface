from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from checkroom.auth import login_required
from checkroom.db import get_db

bp = Blueprint('checkroom', __name__)

@bp.route('/')
def index():
    return render_template('checkroom/index.html')

@bp.route('/checkout')
@login_required
def checkout():
    db = get_db()
    items = db.execute(
        'SELECT * FROM item WHERE user_id = NULL'
        # 'ORDER BY id DESC'
    )
    return str(items)
    return render_template('/checkroom/checkout')

@bp.route('/checkin')
@login_required
def checkin():
    db = get_db()
    items = db.execute(
        'SELECT * FROM item WHERE user_id = ?'
        'ORDER BY id DESC',
        (g.user_id,)
    )
    return str(items)
    return render_template('/checkroom/checkin')