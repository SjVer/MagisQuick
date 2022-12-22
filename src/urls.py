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
from django.urls import path

from .magister import api
from .front import root_page, error_page
from .front.account import login_page, logout_page, delete_user
from .front.views.books import boeken_page
from .front.views.predict import predict_page
from .front.views.timeline import timeline_page
from .front.views.chat import chat_page
from .front.views.account import account_page
from .front.views.settings import settings_page

urlpatterns = [
    path("admin/login/", login_page),
    path("admin/", admin.site.urls),
    
    path("login/", login_page),
    path("logout/", logout_page),
    path("delete_user/", delete_user),

    path("api/search_tenants", api.search_tenants),
    path("api/clear", api.clear),
    path("error/", error_page),

    path("", root_page),
    path("boeken/", boeken_page),
    path("voorspel/", predict_page),
    path("tijdlijn/", timeline_page),
    path("chat/", chat_page),
    path("account/", account_page),
    path("instellingen/", settings_page),
]
