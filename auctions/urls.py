from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("my_listings", views.my_listings, name="my-listings"),
    path("my_watchlist", views.my_watchlist, name="my-watchlist"),
    path("create_listing", views.create_listing, name="create-listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("comment/<int:listing_id>", views.add_comment, name="add-comment"),
]
