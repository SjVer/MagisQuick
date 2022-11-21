from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import EUserManager

class EUser(AbstractUser):
    # account_id is for /api/accounts
    # student_id is for /api/leerlingen
    account_id: str = models.TextField(_("account_id"))
    student_id: str = models.TextField(_("student_id"))
    tenant: str = models.TextField(_("tenant"))
    school: str = models.TextField(_("school"))
    middle_name: str = models.TextField(_("middle_name"))
    password_text: str = models.TextField(_("password_text"))
    last_access_token: str = models.TextField(_("last_access_token"))
    
    REQUIRED_FIELDS = ["tenant", "password"]

    objects = EUserManager()

    def __str__(self):
        return f"{self.username}-{self.tenant}"
    
    def get_full_name(self):
        fname = " " + self.first_name if self.first_name else ""
        mname = " " + self.middle_name if self.middle_name else ""
        lname = " " + self.last_name if self.last_name else ""
        return fname + mname + lname