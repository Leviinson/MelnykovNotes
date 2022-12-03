from django.http import (HttpRequest,
                         HttpResponse)

from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import (Tasks,
                     FriendsRequests,
                     AllowedFriendsToTask)


import uuid


# Create your views here.
@login_required
def func_stub_userprofile(request: HttpRequest, user_uuid: uuid):
    '''
    Returns the user's profile depending on
    whether he is the owner or not returns "owner" variable
    with boolean value.
    '''
    users = get_user_model()
    user_profile = users.objects.get(uuid = user_uuid)
    
    if request.user.uuid == user_uuid: is_owner = True
    else: is_owner = False

    return render(request, 'userprofile/profile.html', {'user': user_profile,
                                                        'tasks': Tasks,
                                                        'friends': user_profile.friends.all(),
                                                        'owner': is_owner})