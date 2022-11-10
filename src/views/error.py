from django.shortcuts import render

def render_error(request, msg):
    return render(request, 'error.html', {
        "message": msg
	})