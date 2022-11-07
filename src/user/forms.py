from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import EUser

class EUserCreationForm(UserCreationForm):

    class Meta:
        model = EUser
        fields = ('email',)


class EUserChangeForm(UserChangeForm):

    class Meta:
        model = EUser
        fields = ('email',)