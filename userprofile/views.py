from django.http import (Http404,
                         HttpRequest,
                         HttpResponseNotFound,
                         HttpResponse)

from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings

from dateutil.relativedelta import relativedelta
from datetime import date 

import uuid

from .models import (Tasks,
                     FriendsRequests,
                     AllowedFriendsToTask)
from .services import define_period_for_relativedelta

# Create your views here.
@login_required
def show_userprofile(request: HttpRequest,
                     user_uuid: uuid.UUID,
                     period: str = settings.SORT_TASKS_LD):
    '''
    Returns the user's profile depending on
    whether he is the owner or not returns "owner" variable
    with boolean value.
    '''

    if period not in (
        settings.SORT_TASKS_LD,
        settings.SORT_TASKS_LW,
        settings.SORT_TASKS_LM,
        settings.SORT_TASKS_LY,
        settings.SORT_TASKS_AT
    ): raise Http404("404 Error...")

    users = get_user_model()
    user_profile = users.objects.get(uuid = user_uuid)
    
    match request.user.uuid == user_uuid:  
        case True:
            is_owner = True

        case False:
            is_owner = False
    
    time_delta = define_period_for_relativedelta(period)
    user_tasks_by_period = Tasks.objects.filter(user_id = user_profile.pk,
                                                date_created__gte = timezone.now() - relativedelta(**time_delta))
    return render(request, 'userprofile/profile.html', {'user': user_profile,
                                                        'tasks': user_tasks_by_period,
                                                        'friends': user_profile.friends.all(),
                                                        'owner': is_owner})


def page_not_found(request, exception):
    return HttpResponseNotFound("404 error")
