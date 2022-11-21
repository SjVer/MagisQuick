from django.shortcuts import render
from django.conf import settings

def render_error(request, msg):
    return render(request, "views/error.html", {
        "settings": settings,
        "title": "Error",
        "message": msg,
	})