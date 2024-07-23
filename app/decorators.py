from django.http import HttpResponseRedirect

def already_loggedin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return wrapper_func