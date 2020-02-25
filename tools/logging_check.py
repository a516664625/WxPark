import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from wx.models import UserProfile

def login_required(view_func):
    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('isLogin'):
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect(reverse('user:login'))

    return wrapper
