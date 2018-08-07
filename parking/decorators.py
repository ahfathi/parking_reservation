from django.http import HttpResponseRedirect
from django.urls import reverse

def staff_required(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('front_view:login'))
        return func(*args, **kwargs)
    return wrapper
