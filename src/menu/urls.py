from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^(?P<path>.*[^/])$', views.redirect_to_trailing_slash),
    re_path(r'.*', views.index, name='index'),
]
