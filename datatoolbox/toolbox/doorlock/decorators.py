from django.http import HttpResponseForbidden
from functools import wraps

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
