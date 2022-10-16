from django.contrib import admin

from .models import EUser
from .forms import EUserCreationForm, EUserChangeForm

class EUserAdmin(admin.ModelAdmin):
	# The forms to add and change user instances
	form = EUserChangeForm()
	add_form = EUserCreationForm()

	# The fields to be used in displaying the CocoUser model.
	# These override the definitions on the base UserAdmin that reference specific fields on auth.User.
	list_display = ('id', 'email', 'is_superuser', 'is_staff',)
	list_filter = ('is_superuser',)
	fieldsets = (
		(None, {'fields': ('is_superuser', 'is_staff', 'email',)}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email')}
		),
	)
	search_fields = ('id', 'email')
	ordering = ('email',)
	filter_horizontal = ()

admin.site.register(EUser, EUserAdmin)