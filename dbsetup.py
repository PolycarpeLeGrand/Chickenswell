from chickenflask import init_app
from chickenflask import db
from chickenflask.home.models import User
from chickenflask.notes.models import NotesCategory, NotesSubcategory, NotesEntry


def make_user():
    print('Creating user')
    name = input('Enter username: ')
    print(f'Entered name: {name}')
    pw1 = input('Enter password: ')
    pw2 = input('Enter password again: ')
    assert pw1 == pw2, 'Passwords dont match'

    new_user = User(name=name)
    new_user.set_password(pw1)
    db.session.add(new_user)
    db.session.commit()
    print(f'Added user {new_user} to database!')


def make_base_cats():
    cat_dict = {
        'Nerd Notes':
            {'rank': 10,
             'subcats': [
                 {'name': 'Raspberry Pi', 'rank': 10},
                 {'name': 'Python Basics', 'rank': 11},
                 {'name': 'Flask and Dash', 'rank': 14},
                 {'name': 'Pandas and Numpy', 'rank': 15},
                 {'name': 'ML and NLP', 'rank': 17},
                 {'name': 'Data Science', 'rank': 18},
                 {'name': 'Frontend', 'rank': 19},
                 {'name': 'Others', 'rank': 21}
                ]
             },
        'Projects':
            {'rank': 11,
             'subcats': [
                 {'name': 'Mempy', 'rank': 10},
                 {'name': 'Memviz', 'rank': 11},
                 {'name': 'Evo Analytics', 'rank': 14},
                 {'name': 'Chickenswell', 'rank': 18},
                ]
             },
        'Mémoire':
            {'rank': 13,
             'subcats': [
                 {'name': 'Explication et Philo', 'rank': 10},
                 {'name': 'Humanités Numériques', 'rank': 11},
                 {'name': 'Organisation', 'rank': 15},
                ]
             },
        'Enseignement':
            {'rank': 15,
             'subcats': [
                 {'name': 'Planification 101', 'rank': 10},
                 {'name': 'Planification 102', 'rank': 11},
                 {'name': 'Planification 103', 'rank': 12},
                 {'name': 'Activités', 'rank': 14},
                 {'name': 'Notes et Théorie', 'rank': 16},
                 {'name': 'Ressources', 'rank': 18},
                 {'name': 'Portfolio', 'rank': 19},
                 {'name': 'Notes de Cours', 'rank': 21},
                ]
             },
        'Varia':
            {'rank': 21,
             'subcats': [
                 {'name': 'Finance', 'rank': 10},
                ]
             },
    }

    for cat, cat_dict in cat_dict.items():
        db.session.add(NotesCategory(name=cat, priority=cat_dict['rank']))

        for sub_cat_dict in cat_dict['subcats']:
            db.session.add(NotesSubcategory(name=sub_cat_dict['name'], parent_name=cat, priority=sub_cat_dict['rank']))

    db.session.commit()
    # print(NotesCategory.query.all())


if __name__ == '__main__':
    app = init_app()
    app.app_context().push()
    db.create_all(app=app)

    if input('Enter y to make new user: ') == 'y':
        make_user()
        print()

    if input('Enter y to make base notes categories: ') == 'y':
        make_base_cats()
