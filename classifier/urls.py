from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('predict/', views.classify_image, name='classify_image'), 
]
