import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rango_project.settings')
django.setup()

from rango.models import Category, Page


def populate():
    python_pages = [
        {
            'title': 'Official Python Tutorial',
            'url': 'http://docs.python.org/3/tutorial/'
        },
        {
            'title': 'How to Think like a Computer Scientist',
            'url': 'http://www.greenteapress.com/thinkpython/'
        },
        {
            'title': 'Learn Python in 10 Minutes',
            'url': 'http://www.korokithakis.net/tutorials/python/'
        }
    ]

    django_pages = [
        {
            'title': 'Official Django Tutorial',
            'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'
        },
        {
            'title': 'Django Rocks',
            'url': 'http://www.djangorocks.com/'
        },
        {
            'title': 'How to Tango with Django',
            'url': 'http://www.tangowithdjango.com/'
        }
    ]

    other_pages = [
        {
            'title': 'Bottle',
            'url': 'http://bottlepy.org/docs/dev/'
        },
        {
            'title': 'Flask',
            'url': 'http://flask.pocoo.org'
        }
    ]

    cats = {
        'Python': {'pages': python_pages},
        'Django': {'pages': django_pages},
        'Other Frameworks': {'pages': other_pages}
    }

    # Save each category and their associated pages to the database
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for page in cat_data['pages']:
            add_page(c, page['title'], page['url'])

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


def add_cat(name):
    cat = Category.objects.get_or_create(name=name)[0]
    cat.save()
    return cat


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
