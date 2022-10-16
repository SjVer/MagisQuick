from django.forms import BaseModelForm
from .models import EUser


class EUserCreationForm(BaseModelForm):
    class Meta:
        model = EUser
        fields = ("email",)


class EUserChangeForm(BaseModelForm):
    class Meta:
        model = EUser
        fields = ("email",)
