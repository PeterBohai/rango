from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('restricted/', views.restricted, name='restricted'),
    path('goto/', views.goto_url, name='goto'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('register_profile/', views.register_profile, name='register_profile')
]