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
                     requested_user_uuid: uuid.UUID,
                     period_abbreviature: str = settings.DEFAULT_PERIOD.abbreviature):
    '''
    Returns:
    --------
        the user's profile depending on whether
        he is the owner or not.
    
    Parameters:
    -----------
        request: HttpRequest
            
        requested_user_uuid: uuid.UUID

        period_abbreviature: str
    '''
    if period_abbreviature not in (
        settings.DICT_OF_PERIODS.keys()
    ): raise Http404("404 Error...")
    context = get_context_for_userprofile_page(request, period_abbreviature, requested_user_uuid)
    return render(request, 'userprofile/profile.html', context = context)


def page_not_found(request, exception):
    return HttpResponseNotFound("404 error")
