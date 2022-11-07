from django.shortcuts import redirect

def root_view(request):
    # if logged in: redirect to home page
    if request.user.is_authenticated:
        print(type(request))
        return redirect('/boeken/')

    # if not logged in: redirect to login page
    return redirect('/login/')