from django.urls import path
from main import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'), 
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('links/', views.links, name='links'),
    path('shop/', views.shop, name='shop'),
    path('services/', views.services, name='services'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('admin/', admin.site.urls),
    path('registration/', views.registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]