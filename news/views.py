from django.http import (
                        HttpRequest,
                        HttpResponse
                        )
from django.shortcuts import render

# Create your views here.
app_name = 'news'
def func_stub_news(request: HttpRequest):
    return HttpResponse("News page")