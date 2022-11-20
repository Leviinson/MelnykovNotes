from django.http import (
                        HttpRequest,
                        )
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


import uuid


# Create your views here.
@login_required
def func_stub_userprofile(request: HttpRequest, user_uuid: uuid):
    if request.user.uuid == user_uuid:
        pass
    else:
        pass
    return render(request, 'userprofile/profile.html', {'user': get_user_model()})