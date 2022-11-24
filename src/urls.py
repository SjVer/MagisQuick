"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""

from django.contrib import admin
from django.urls import path, include

from .magister import api
from .front import root_page, error_page
from .front.account import login_page, logout_page
from .front.views.account import account_page
from .front.views.boeken import boeken_page

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # included views:
    #   login/ [name="login"]
    #   logout/ [name="logout"]
    #   password_change/ [name="password_change"]
    #   password_change/done/ [name="password_change_done"]
    #   password_reset/ [name="password_reset"]
    #   password_reset/done/ [name="password_reset_done"]
    #   reset/<uidb64>/<token>/ [name="password_reset_confirm"]
    #   reset/done/ [name="password_reset_complete"]
    # path("", include("django.contrib.auth.urls")),
    path("login/", login_page),
    path("logout/", logout_page),

    path("api/search_tenants", api.search_tenants),
    path("error/", error_page),

    path("", root_page),
    path("account/", account_page),
    path("boeken/", boeken_page),
]
