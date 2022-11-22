from django.conf import settings

if settings.DEBUG:
    __import__("os").system("clear")

