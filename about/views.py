from django.http import (
                        HttpRequest,
                        HttpResponse
                        )
from django.shortcuts import render

app_name = 'about'
# Create your views here.
def func_stub_about(request: HttpRequest):
    return HttpResponse("About page")