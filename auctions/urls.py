from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("", views.index, name="index"),
    path("my_listings", views.my_listings, name="my-listings"),
    path("create_listing", views.create_listing, name="create-listing"),
]
