from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask import current_app as app
from flask_login import current_user, login_required
from .models import db, NotesCategory, NotesSubcategory, NotesEntry
from .forms import NotesEntryForm, NotesDeleteForm, CategoryEntryForm, SubcategoryEntryForm, CatDeleteForm


# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@app.context_processor
def notes_sidebar_processor():
    if current_user.is_authenticated:
        d = {cat.name: {subcat.name: {entry.name: url_for('home_bp.notes', cat=cat.name, subcat=subcat.name, entry=entry.name) for entry in subcat.entries} for subcat in cat.sub_categories}
             for cat in NotesCategory.query.order_by(NotesCategory.priority).all()}
    else:
        d = {}
    return {'dropdowns': d}


@home_bp.route('/', methods=['GET'])
# @login_required
def home():
    return render_template('home/home.jinja2')


@home_bp.route('/markdown', methods=['GET'])
@login_required
def markdown_view():
    entry = NotesEntry.query.filter_by(name='Markdown').first_or_404()
    subcat = NotesSubcategory.query.filter_by(name=entry.category_name).first_or_404()
    cat = subcat.category_name
    return redirect(url_for('home_bp.notes', cat=cat, subcat=subcat.name, entry=entry.name))


@home_bp.route('/notes/<string:cat>/<string:subcat>/<string:entry>', methods=['GET'])
@login_required
def notes(cat, subcat, entry):
    e = NotesEntry.query.filter_by(name=entry).first_or_404()
    return render_template('home/notes.jinja2', category=cat, subcategory=subcat, entry=e, title=e.name)


@home_bp.route('/notes/manage', methods=['GET'])
@login_required
def manage_notes():
    entry_form = NotesEntryForm()
    delete_form = NotesDeleteForm()
    category_form = CategoryEntryForm()
    subcategory_form = SubcategoryEntryForm()
    cat_delete_form = CatDeleteForm()
    return render_template('home/notesmanager.jinja2', entry_form=entry_form, delete_form=delete_form,
                           category_form=category_form, subcategory_form=subcategory_form, cat_delete_form=cat_delete_form)


@home_bp.route('/notes/manage/addentry', methods=['GET', 'POST'])
@login_required
def manage_notes_add_entry():
    form = NotesEntryForm()
    if request.method == 'POST' and form.is_submitted():
        try:
            new_entry = NotesEntry(name=form.name.data, drive_url=form.drive_url.data, category_name=form.subcategory.data)
            db.session.add(new_entry)
            db.session.commit()
            flash(f'Success! Added {new_entry.name} in {form.category.data} - {form.subcategory.data}')
        except Exception as err:
            flash(f'Error! {err}')
    return redirect(url_for('home_bp.manage_notes'))


@home_bp.route('/notes/manage/addcategory', methods=['GET', 'POST'])
@login_required
def manage_notes_add_category():
    form = CategoryEntryForm()
    if request.method == 'POST' and form.is_submitted():
        try:
            new_entry = NotesCategory(name=form.name.data)
            db.session.add(new_entry)
            db.session.commit()
            flash(f'Success! Created new category: {new_entry.name}')
        except Exception as err:
            flash(f'Error! {err}')
    return redirect(url_for('home_bp.manage_notes'))


@home_bp.route('/notes/manage/addsubcategory', methods=['GET', 'POST'])
@login_required
def manage_notes_add_subcategory():
    form = SubcategoryEntryForm()
    if request.method == 'POST' and form.is_submitted():
        try:
            new_entry = NotesSubcategory(name=form.name.data, category_name=form.category.data)
            db.session.add(new_entry)
            db.session.commit()
            flash(f'Success! Created new subcategory: {new_entry.name} ({new_entry.category_name})')
        except Exception as err:
            flash(f'Error! {err}')
    return redirect(url_for('home_bp.manage_notes'))


@home_bp.route('/notes/manage/deleteentry', methods=['GET', 'POST'])
@login_required
def manage_notes_delete_entry():
    form = NotesDeleteForm()
    if request.method == 'POST' and form.is_submitted():
        try:
            entry = NotesEntry.query.filter_by(name=form.name.data).first()
            db.session.delete(entry)
            db.session.commit()
            flash(f'Success! Deleted {entry.name}')
        except Exception as err:
            flash(f'Error! {err}')
    return redirect(url_for('home_bp.manage_notes'))


@home_bp.route('/notes/manage/deletecat', methods=['GET', 'POST'])
@login_required
def manage_notes_delete_cat():
    form = CatDeleteForm()
    if request.method == 'POST' and form.is_submitted():
        try:
            if form.model_type.data == 'category':
                c = NotesCategory.query.filter_by(name=form.name.data).first()
                assert len(c.sub_categories) == 0
            else:
                c = NotesSubcategory.query.filter_by(name=form.name.data).first()
                assert len(c.entries) == 0
            db.session.delete(c)
            db.session.commit()
            flash(f'Success! Deleted {c.name}')
        except Exception as err:
            flash(f'Error! {err}')
    return redirect(url_for('home_bp.manage_notes'))



@home_bp.route('/notes/manage/update/<string:id>', methods=['GET'])
@login_required
def manage_notes_update(id):
    entry = NotesEntry.query.filter_by(id=id).first()
    entry.update_content()
    db.session.commit()
    flash(f'Entry updated')

    return redirect(request.referrer)
    #return redirect(next_page or url_for('home_bp.home'))


