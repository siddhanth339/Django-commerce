from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name = "createListing"),
    path("listings/<int:id>", views.listing, name = "listings"),
    path("add/<int:id>", views.addToWatchList, name = "add"),
    path("watchList", views.show_watchList, name = "show_watchList")
]
