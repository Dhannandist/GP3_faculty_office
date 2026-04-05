from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.conf import settings


def login_required(view):
    """
    This is a decorator that checks and ensure that
    a user must be logged in to access a view
    """

    @wraps(view)
    def _wrapped_view(req, *args, **kwargs):
        if not req.user.is_authenticated:
            messages.error(req, settings.LOGIN_REDIRECT_MSG)
            return redirect(settings.LOGIN_VIEW_NAME)
        return view(req, *args, **kwargs)

    return _wrapped_view
