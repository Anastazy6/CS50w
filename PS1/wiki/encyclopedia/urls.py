from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new_page, name="new-page"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("random/", views.random, name="random")
]
