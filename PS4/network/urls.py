
from django.urls import path

from . import views

urlpatterns = [
    path("",          views.index,       name="index"),
    path("login",     views.login_view,  name="login"),
    path("logout",    views.logout_view, name="logout"),
    path("register",  views.register,    name="register"),
    path("new-post",  views.new_post,    name="new-post"),
    path("follow",    views.follow,      name="follow"),
    path("following", views.following,   name="following"),
    
    # Used to dynamically generate reaction categories for the reaction iterface
    #   should site admin add, remove or modify them.
    path("get-rcategories", views.get_rcategories, name="get-rcategories"),
    
    path("profile/"    "<int:profile_id>", views.profile,       name="profile"),
    path("edit/"       "<int:post_id>",    views.edit_post,     name="edit-post"),
    path("like/"       "<int:post_id>",    views.like_post,     name="like-post"),
    path("react/"      "<int:post_id>",    views.react_to_post, name="react-to-post"),
    path("get_reactions/<int:post_id>",    views.get_reactions, name="get-reactions"),
    path("shadowban/"  "<int:target_id>",  views.shadowban,     name="shadowban")
]
