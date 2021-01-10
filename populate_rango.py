import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rango_project.settings')
django.setup()

from rango.models import Category, Page


def populate():
    python_pages = [
        {
            'title': 'Official Python Tutorial',
            'url': 'http://docs.python.org/3/tutorial/',
            'views': 23
        },
        {
            'title': 'How to Think like a Computer Scientist',
            'url': 'http://www.greenteapress.com/thinkpython/',
            'views': 434
        },
        {
            'title': 'Learn Python in 10 Minutes',
            'url': 'http://www.korokithakis.net/tutorials/python/',
            'views': 13
        }
    ]

    django_pages = [
        {
            'title': 'Official Django Tutorial',
            'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
            'views': 89
        },
        {
            'title': 'Django Rocks',
            'url': 'http://www.djangorocks.com/',
            'views': 9
        },
        {
            'title': 'How to Tango with Django',
            'url': 'http://www.tangowithdjango.com/',
            'views': 327
        }
    ]

    other_pages = [
        {
            'title': 'Bottle',
            'url': 'http://bottlepy.org/docs/dev/',
            'views': 2373
        },
        {
            'title': 'Flask',
            'url': 'http://flask.pocoo.org',
            'views': 2
        }
    ]

    cats = {
        'Python': {
            'pages': python_pages,
            'views': 128,
            'likes': 64
        },
        'Django': {
            'pages': django_pages,
            'views': 64,
            'likes': 32
        },
        'Other Frameworks': {
            'pages': other_pages,
            'views': 32,
            'likes': 16
        },
        'Perl': {
            'pages': [],
            'views': 1,
            'likes': 9
        },
        'PHP': {
            'pages': [],
            'views': 2,
            'likes': 7
        },
        'Prolog': {
            'pages': [],
            'views': 1,
            'likes': 5
        },
        'PostScript': {
            'pages': [],
            'views': 3,
            'likes': 42
        },
        'Programming': {
            'pages': [],
            'views': 3,
            'likes': 323
        },
        'Puppies': {
            'pages': [],
            'views': 6,
            'likes': 2
        },
        'Another One': {
            'pages': [],
            'views': 4,
            'likes': 3
        },
    }

    # Save each category and their associated pages to the database
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data)
        for page in cat_data['pages']:
            add_page(c, page['title'], page['url'], page['views'])

    # Display all the newly added objects
    for cat in Category.objects.all():
        for page in Page.objects.filter(category=cat):
            print(f'- {cat}: {page}')


def add_page(cat, title, url, views=0):
    page = Page.objects.get_or_create(category=cat, title=title)[0]
    page.url = url
    page.views = views
    page.save()
    return page


def add_cat(name, data):
    cat = Category.objects.get_or_create(name=name)[0]
    cat.likes = data.get('likes', 0)
    cat.views = data.get('views', 0)
    cat.save()
    return cat


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
