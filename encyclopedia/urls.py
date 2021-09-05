from django.conf.urls import handler500
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("random/", views.random, name="random"),
    path("delete_page/", views.delete_page, name="delete_page"),
]
