"""Routes for user authentication."""
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from .forms import LoginForm
from .models import db, User
from chickenflask import login_manager
#from .forms import LoginForm, SignupForm
#from .models import User, db


# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """

    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home_bp.home'))
        # flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template(
        'home/login.jinja2',
        form=form,
        title='Log in',
        template='login-page',
        body="Log in with your User account."
    )


@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.home'))


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    # flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))

