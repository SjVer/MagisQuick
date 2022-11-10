from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class EUserManager(BaseUserManager):
    def create_user(self, tenant, username, password, **extra_fields):
        if not tenant: raise ValueError(_('The tenant must be set'))
        if not username: raise ValueError(_('The username must be set'))

        user = self.model(
            tenant=tenant,
            username=username,
            password_text=password,
            **extra_fields
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, tenant, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(tenant, username, password, **extra_fields)