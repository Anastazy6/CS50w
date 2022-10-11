from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-auction", views.create_auction, name="create-auction"),
    path("auction/<int:auction_id>", views.auction_view, name="view-auction"),
    path("watchlist", views.watchlist_view, name="view-watchlist"),
    path("category/<str:category>", views.category_view, name="view-category"),
    path("won-auctions", views.won_auctions_view, name="view-won-auctions")
]
urlpatterns += staticfiles_urlpatterns()