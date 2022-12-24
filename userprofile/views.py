from django.http import (Http404,
                         HttpRequest,
                         HttpResponseNotFound,
                         HttpResponse)

from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings

import uuid

from .services import get_user_tasks_by_period
from .typehints import PeriodsOfTasks


# Create your views here.
@login_required
def show_userprofile(request: HttpRequest,
                     user_uuid: uuid.UUID,
                     period: PeriodsOfTasks = settings.SORT_TASKS_TD):
    '''
    Returns the user's profile depending on
    whether he is the owner or not returns "owner" variable
    with boolean value.
    '''
    if period not in (
        settings.SORT_TASKS_TD,
        settings.SORT_TASKS_TW,
        settings.SORT_TASKS_TM,
        settings.SORT_TASKS_TY,
        settings.SORT_TASKS_AT
    ): raise Http404("404 Error...")

    context = get_user_tasks_by_period(request, period, user_uuid)
    return render(request, 'userprofile/profile.html', context = context)


def page_not_found(request, exception):
    return HttpResponseNotFound("404 error")
