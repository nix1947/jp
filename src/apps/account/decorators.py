from django.core.exceptions import PermissionDenied
from apps.account import usertype


def employer_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type == usertype.EMPLOYER:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrapper


def jobseeker_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type == usertype.JOBSEEKER:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrapper


def owner_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.id == kwargs['pk']:
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrapper
