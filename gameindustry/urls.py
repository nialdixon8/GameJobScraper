#Importing from django.urls path to map URLs to views
#Note: View in django is not the same as view in Spring.
#Views behave as request handlers
from django.urls import path
from . import views

#URLconf
urlpatterns = [
    path('', views.homepage),
    path('scrape', views.scrape),
    path('create_filter', views.create_filter),
]
