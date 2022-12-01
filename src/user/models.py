from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models

from .manager import EUserManager

class EUser(AbstractUser):
    username = username = models.TextField(_("username"))
    # account_id is for /api/accounts
    # student_id is for /api/leerlingen
    account_id: str = models.TextField(_("account_id"))
    student_id: str = models.TextField(_("student_id"))
    tenant: str = models.TextField(_("tenant"))
    school: str = models.TextField(_("school"))
    school_id: str = models.TextField(_("school_id"))
    middle_name: str = models.TextField(_("middle_name"))
    password_text: str = models.TextField(_("password_text"))
    refresh_token: str = models.TextField(_("refresh_token"))
    
    REQUIRED_FIELDS = ["school"]
    SCHOOL_FIELD = "school"

    objects = EUserManager()

    def __str__(self):
        return f"{self.username} - {self.school}"
    
    def get_full_name(self):
        fname = " " + self.first_name if self.first_name else ""
        mname = " " + self.middle_name if self.middle_name else ""
        lname = " " + self.last_name if self.last_name else ""
        return fname + mname + lname

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        unique_together = ("username", "school")

admin.site.register(EUser)