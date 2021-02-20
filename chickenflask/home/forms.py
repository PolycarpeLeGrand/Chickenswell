"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import (
    DataRequired,
    Email,
    URL,
    EqualTo,
    Length,
    Optional
)


class LoginForm(FlaskForm):
    """User Log-in Form."""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )

    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
