from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('links/', views.links, name='links'),
    path('shop/', views.shop, name='shop'),
    path('services/', views.services, name='services'),
    path('feedback/', views.feedback_view, name='feedback')
]

