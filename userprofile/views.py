from django.http import (
                        HttpRequest,
                        HttpResponse
                        )
from django.shortcuts import render

# Create your views here.
def func_stub_userprofile(request: HttpRequest):
    return HttpResponse("User profile page")