from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.conf import settings


def admin_required(view):
    """
    This is a decorator that checks and ensure that
    a user must be logged in to access a view
    """

    @wraps(view)
    def _wrapped_view(req, *args, **kwargs):
        # If not admin
        if req.user.role != "ADMIN":
            messages.error(req, "You're not an admin!")
            return redirect("dashboard")

        # If admin
        return view(req, *args, **kwargs)

    return _wrapped_view
