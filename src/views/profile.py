from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .error import render_error
from .. import magister

@login_required
def profile_view(request):
	session = magister.MagisterSession(request.user)
	session.authenticate()

	if not session: return render_error(request, "auth failed")

	session.update_userinfo()
	return render(request, "profile.html", {
        "user": session.user,
		"full_name": session.user.get_full_name()
	})