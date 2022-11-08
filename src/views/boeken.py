from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .. import magister

@login_required
def boeken_view(request):
    print(magister.get_session("CSG Willem van Oranje", "22572", "Sj03rd@WvO.sv"))
    # print(magister.get_session("dewillem", "22572", "Sj03rd@WvO.sv"))
    return render(request, 'boeken.html', {
		'user': request.user
	})