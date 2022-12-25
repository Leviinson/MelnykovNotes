from django.http import (Http404,
                         HttpRequest,
                         HttpResponseNotFound)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

import uuid

from .services import get_context_for_userprofile_page


# Create your views here.
@login_required
def show_userprofile(request: HttpRequest,
                     user_uuid: uuid.UUID,
                     period_abbreviature: str = settings.TASKS_PERIODS['this_day']['abbreviature']):
    '''
    Returns:
    --------
        the user's profile depending on whether
        he is the owner or not.
    
    Parameters:
    -----------
        request: HttpRequest
            
        user_uuid: uuid.UUID

        period: str
    '''
    if period_abbreviature not in (
        settings.TASKS_PERIODS[period]['abbreviature'] for period
        in settings.TASKS_PERIODS
    ): raise Http404("404 Error...")
    context = get_context_for_userprofile_page(request, period_abbreviature, user_uuid)
    return render(request, 'userprofile/profile.html', context = context)


def page_not_found(request, exception):
    return HttpResponseNotFound("404 error")
