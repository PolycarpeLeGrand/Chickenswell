from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask import current_app as app
from flask_login import current_user, login_required
from .models import db


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@home_bp.route('/', methods=['GET'])
# @login_required
def home():
    return render_template('home/home.jinja2')




