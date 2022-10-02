from django.shortcuts import redirect

def root_view(request):
    # if logged in: redirect to home page

    # if not logged in: redirect to login page
	return redirect('/login/')