from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .. import magister

@login_required
def boeken_view(request):
	session = magister.MagisterSession()
	session.authenticate("CSG Willem van Oranje", "22572", "Sj03rd@WvO.sv")
 
	return render(request, 'boeken.html', {
		'userinfo': session.get_userinfo()
	})