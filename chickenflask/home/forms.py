"""Sign-up & log-in forms."""
from .models import NotesCategory
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


class NotesEntryForm(FlaskForm):
    """Notes entry form"""

    name = StringField(
        'Name',
        validators=[DataRequired()]
    )

    drive_url = StringField(
        'Drive Url',
        validators=[DataRequired(), URL()]
    )

    category = SelectField(
        'Category',
        validators=[DataRequired()]
    )

    subcategory = SelectField(
        'Subcategory',
        validators=[DataRequired()]
    )
    submit = SubmitField('Add Entry')

    def __init__(self, **kwargs):
        super(NotesEntryForm, self).__init__(**kwargs)
        self.category.choices = [(cat.name, cat.name) for cat in NotesCategory.query.all()]


class CategoryEntryForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    submit = SubmitField('Add Category')


class SubcategoryEntryForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    category = SelectField(
        'Category',
        validators=[DataRequired()]
    )
    submit = SubmitField('Add Subcategory')

    def __init__(self, **kwargs):
        super(SubcategoryEntryForm, self).__init__(**kwargs)
        self.category.choices = [(cat.name, cat.name) for cat in NotesCategory.query.all()]


class NotesDeleteForm(FlaskForm):
    """Notes delete form"""

    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    submit = SubmitField('Delete Entry')


class CatDeleteForm(FlaskForm):
    """Category and subcategory delete form"""

    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    model_type = SelectField(
        'Cat or Subcat',
        choices=[('category', 'Category'), ('subcategory', 'Subcategory')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Delete Cat / Subcat')