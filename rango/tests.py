from django.test import TestCase
from rango.models import Category, Page
from django.urls import reverse
from django.utils import timezone


class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """Ensures the number of views for a Category is non-negative."""
        category = add_category('test', -1, 0)

        self.assertEqual(category.views >= 0, True)

    def test_slug_line_creation(self):
        """Checks that an appropriate slug is created when a category is created.

        Example: "Random Category String" should become "random-category-string"
        """
        category = add_category('Random Category String')

        self.assertEqual(category.slug, 'random-category-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """If no categories exist, the appropriate message should be displayed."""
        response = self.client.get(reverse('rango:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """Checks whether categories are dsiplayed correctly when present."""
        add_category('Python', 1, 1)
        add_category('C++', 1, 1)
        add_category('Erlang')

        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python')
        self.assertContains(response, 'C++')
        self.assertContains(response, 'Erlang')

        num_categories = len(response.context['categories'])
        self.assertEqual(num_categories, 3)


class PageMethodTests(TestCase):
    def test_ensure_last_view_not_future(self):
        """Ensures that the last_visit field of a page cannot be in the future."""
        category = add_category('test', 1, 2)
        page = add_page(category, 'Test Page', 'http://www.google.com')

        self.assertTrue(page.last_visit < timezone.now())

    def test_ensure_las_visit_updated_when_requested(self):
        """Ensures that the last_visit field is updated correctly when a page is requested."""
        category = add_category('test', 1, 2)
        page = add_page(category, 'Test Page', 'http://www.google.com')
        creation_date = page.last_visit

        self.client.get(reverse('rango:goto'), {'page_id': 1})
        page.refresh_from_db()

        self.assertTrue(page.last_visit > creation_date)


# Helper functions
def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes
    category.save()
    return category


def add_page(category, title, url, views=0):
    page = Page.objects.get_or_create(category=category, title=title, url=url)[0]
    page.views = views
    page.save()
    return page
