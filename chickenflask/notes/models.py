from chickenflask import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .drivesync import sync_new_file, create_new_drive_file, upload_content_to_drive
from config import DRIVE_FOLDER_ID
from datetime import datetime


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

    parent_name = db.Column(db.String(100), db.ForeignKey('notes-categories.name'),
                            nullable=False)
    entries = db.relationship('NotesEntry', backref=db.backref('parent'), lazy=True)


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

    parent_name = db.Column(db.String(100), db.ForeignKey('notes-subcategories.name'),
                            nullable=False)

    def __init__(self, **kwargs):
        super(NotesEntry, self).__init__(**kwargs)
        if self.drive_url == '':
            self.add_to_drive_as_new_file()
        else:
            self.get_content_from_drive()

    def get_content_from_drive(self):
        self.content, self.content_type = sync_new_file(self.drive_url)
        # self.last_update = datetime.now (if success)
        self.last_update = datetime.now()

    def save_and_sync_content(self, new_content):
        self.content = new_content
        upload_content_to_drive(self.content, self.drive_url)
        self.last_update = datetime.now()

    def add_to_drive_as_new_file(self):
        self.content = f'{self.name}\n{len(self.name)*"="}'
        self.drive_url = create_new_drive_file(self.content, self.name, DRIVE_FOLDER_ID)
        self.last_update = datetime.now()

    def get_last_updated(self):
        return self.last_update.strftime("%Y-%m-%d %H:%M") if self.last_update else None

    def __repr__(self):
        return f'Entry: {self.name}'

