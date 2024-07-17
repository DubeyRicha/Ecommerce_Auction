from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.category_list, name="category_list"),
    path("category/<str:categoryname>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:list_id>",views.watch, name="watch"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listing/<int:list_id>", views.listing, name="listing"),
    path("bid/<int:list_id>", views.bid, name="bid"),
    path("close/<int:list_id>", views.close, name="close"),
     path("comment/<int:list_id>", views.comment, name="comment"),
]
