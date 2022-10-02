from django.forms import ModelForm
from .models import EUser

class EUserCreationForm(ModelForm):

    class Meta:
        model = EUser
        fields = ("email",)

class EUserChangeForm(ModelForm):

    class Meta:
        model = EUser
        fields = ("email",)