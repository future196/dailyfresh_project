# from django.http import request
from django.shortcuts import redirect
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('username'):
            return func(request, *args, **kwargs)
        else:
            red = redirect("/user/login/")
            red.set_cookie('url', request.get_full_path)
            return red

    return wrapper