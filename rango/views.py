from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from rango.models import Category, Page, UserProfile, User
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.bing_search import run_query


class IndexView(View):
    def get(self, request):
        # Retrieve a list of the top 5 liked catgories
        category_list = Category.objects.order_by('-likes')[:5]
        page_list = Page.objects.order_by('-views')[:5]

        visitor_cookie_handler(request)
        context_dict = {
            'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
            'categories': category_list,
            'pages': page_list
        }

        return render(request, 'rango/index.html', context=context_dict)


class RestrictedView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'rango/restricted.html')


class ShowCategoryView(View):
    def create_context_dict(self, category_name_slug):
        context_dict = {}

        try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category).order_by('-views')

            context_dict['pages'] = pages
            context_dict['category'] = category
        except Category.DoesNotExist:
            context_dict['pages'] = None
            context_dict['category'] = None

        return context_dict

    def get(self, request, category_name_slug):
        context_dict = self.create_context_dict(category_name_slug)
        return render(request, 'rango/category.html', context=context_dict)

    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        context_dict = self.create_context_dict(category_name_slug)
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['result_list'] = result_list
            context_dict['prev_query'] = query

        return render(request, 'rango/category.html', context=context_dict)


class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        return render(request, 'rango/add_category.html', {'form': form})


class AddPageView(View):
    form_class = PageForm

    def get_category_name(self, category_name_slug):
        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category = None

        return category

    def create_context_dict(self, form, category):
        return {
            'form': form,
            'category': category
        }

    @method_decorator(login_required)
    def get(self, request, category_name_slug):
        category = self.get_category_name(category_name_slug)
        if not category:
            return redirect(reverse('rango:index'))
        form = self.form_class()
        return render(request, 'rango/add_page.html', context=self.create_context_dict(form, category))

    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        category = self.get_category_name(category_name_slug)
        form = self.form_class(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()

            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

        return render(request, 'rango/add_page.html', context=self.create_context_dict(form, category))


class AboutView(View):
    def get(self, request):
        visitor_cookie_handler(request)
        context_dict = {
            'boldmessage': 'This tutorial has been put together by Peter Hu',
            'visits': request.session['visits']
        }
        return render(request, 'rango/about.html', context=context_dict)


class GoToUrlView(View):
    def get(self, request):
        page_id = request.GET.get('page_id')
        try:
            page = Page.objects.get(pk=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('rango:index'))
        page.views += 1
        page.last_visit = timezone.now()
        page.save()
        return redirect(page.url)


class RegisterProfileView(View):
    form_class = UserProfileForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        return render(request, 'rango/profile_registration.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
        return render(request, 'rango/profile_registration.html', {'form': form})


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({
            'website': user_profile.website,
            'picture': user_profile.picture
        })

        return user, user_profile, form

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        context_dict = {
            'selected_user': user,
            'user_profile': user_profile,
            'form': form
        }
        return render(request, 'rango/profile.html', context=context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid() and user == request.user:
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)

        context_dict = {
            'selected_user': user,
            'user_profile': user_profile,
            'form': form
        }
        return render(request, 'rango/profile.html', context=context_dict)


class ProfileListView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()
        return render(request, 'rango/profile_list.html', context={'user_profiles': profiles})


class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET.get('category_id')

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        except TypeError:
            return HttpResponse(-1)

        category.likes += 1
        category.save()

        return HttpResponse(category.likes)


class CategorySuggestionView(View):
    def get(self, request):
        suggestion = request.GET.get('suggestion', '')
        category_list = get_category_list(max_results=8, starts_with=suggestion)

        if len(category_list) == 0:
            category_list = Category.objects.order_by('-likes')

        return render(request, 'rango/categories.html', {'categories': category_list})


class SearchAddPageView(View):
    def get(self, request):
        category_id = request.GET.get('category_id')
        title = request.GET.get('title')
        url = request.GET.get('url')
        print('HEREE')

        try:
            category = Category.objects.get(pk=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse('Error - category not found.')
        except ValueError:
            return HttpResponse('Error - bad category ID.')
        except TypeError:
            return HttpResponse('Error - no category ID query string found')

        Page.objects.get_or_create(title=title, url=url, category=category)
        pages = Page.objects.filter(category=category).order_by('-views')
        return render(request, 'rango/page_listing.html', {'pages': pages})


# Helper Functions
def visitor_cookie_handler(request):
    visits = request.session.get('visits', 1)
    last_visit_cookie = request.session.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def get_category_list(max_results=0, starts_with=''):
    category_list = []
    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]
    return category_list

