from django.http import (
                        HttpRequest,
                        )
from django.shortcuts import render

# Create your views here.
def func_stub_userprofile(request: HttpRequest):
    return render(request, 'userprofile/profile.html', {})