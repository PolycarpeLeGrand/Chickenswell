"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle


def compile_static_assets(assets):
    """Create stylesheet bundles."""

    common_less_bundle = Bundle(
        'src/less/style.less',
        filters='less,cssmin',
        output='dist/css/style.css',
        depends='src/less/stylelib.less',
        extra={'rel': 'stylesheet/less',}
    )
    home_less_bundle = Bundle(
        'home_bp/src/less/home.less',
        filters='less,cssmin',
        output='dist/css/home.css',
        extra={'rel': 'stylesheet/less'}
    )
    auth_less_bundle = Bundle(
        'home_bp/src/less/login.less',
        filters='less,cssmin',
        output='auth_bp/dist/css/login.css',
        extra={'rel': 'stylesheet/less'}
    )
    notes_less_bundle = Bundle(
        'notes_bp/src/less/notes.less',
        'notes_bp/src/less/notesmanager.less',
        filters='less,cssmin',
        output='notes_bp/dist/css/notes.css',
        extra={'rel': 'stylesheet/less'}
    )
    assets.register('common_less', common_less_bundle)
    assets.register('home_less', home_less_bundle)
    assets.register('auth_less', auth_less_bundle)
    assets.register('notes_less', notes_less_bundle)
    if app.config['FLASK_ENV'] == 'development':
        common_less_bundle.build()
        home_less_bundle.build()
        auth_less_bundle.build()
        notes_less_bundle.build()
    return assets

