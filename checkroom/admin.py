from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for
)
from werkzeug.exceptions import abort

from checkroom.auth import login_required, admin_required
from checkroom.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route("/")
@admin_required
def index():
    return render_template('admin/index.html')