from chickenflask import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .drivesync import sync_new_file


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin-users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class NotesCategory(db.Model):

    __tablename__ = 'notes-categories'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    priority = db.Column(
        db.Integer,
        default=20,
        nullable=False
    )

    sub_categories = db.relationship('NotesSubcategory', backref='parent', lazy=True)
    # parent = db.relationship('NotesCategory')
    #parent = db.relationship('NotesCategory', backref=db.backref('sub_categories'))
    #entries = db.relationship('NotesEntry')

    def __repr__(self):
        return f'Category: {self.name} | ID: {self.id} | Priority: {self.priority} | Associated Subcategories: {", ".join(subcat.name for subcat in self.sub_categories)}'


class NotesSubcategory(db.Model):

    __tablename__ = 'notes-subcategories'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    priority = db.Column(
        db.Integer,
        default=20,
        nullable=False
    )

    entries = db.relationship('NotesEntry', backref=db.backref('parent'), lazy=True)
    category_name = db.Column(db.String(100), db.ForeignKey('notes-categories.name'),
        nullable=False)

    def __repr__(self):
        return f'Subcategory: {self.name} | Priority: {self.priority} | Associated notes: {", ".join(entry.name for entry in self.entries)}'


class NotesEntry(db.Model):

    __tablename__ = 'notes-entries'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False,
        default=''
    )

    #markdown or html
    content_type = db.Column(
        db.String(100),
        unique=False,
        nullable=False,
        default='markdown'
    )

    last_update = db.Column(
        db.DateTime,
    )

    drive_url = db.Column(
        db.String(200),
        unique=True,
        default='#'
    )

    category_name = db.Column(db.String(100), db.ForeignKey('notes-subcategories.name'),
                              nullable=False)

    def __init__(self, **kwargs):
        super(NotesEntry, self).__init__(**kwargs)
        self.update_content()

    def update_content(self):
        self.content, self.content_type = sync_new_file(self.drive_url)
        # self.last_update = datetime.now (if success)

    def __repr__(self):
        return f'Entry: {self.name}'

