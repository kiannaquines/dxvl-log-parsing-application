from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

def already_loggedin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('dashboard'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func